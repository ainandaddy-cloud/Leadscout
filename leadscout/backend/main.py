"""
LeadScout Backend — FastAPI
Run: uvicorn main:app --reload --port 8000
Place this file inside: leadscout/backend/
"""

import asyncio
import sys
import json
import os
import csv
import uuid
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="LeadScout API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH    = "leadscout.db"
OUTPUT_DIR = Path("../output")
OUTPUT_DIR.mkdir(exist_ok=True)
active_jobs = {}

EVENT_BUFFER_LIMIT = 800
WS_QUEUE_MAXSIZE = 120


def _env_int(name: str, default: int, min_value: int, max_value: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(min_value, min(max_value, value))


DB_FLUSH_EVERY = _env_int("LEADSCOUT_DB_FLUSH_EVERY", 80, 10, 500)
AREA_CONCURRENCY = _env_int("LEADSCOUT_AREA_CONCURRENCY", 2, 1, 10)


def _safe_slug(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in (value or ""))
    return cleaned.strip("_") or "leads"


def build_job_csv_path(niche: str, job_id: str) -> str:
    return str(OUTPUT_DIR / f"{_safe_slug(niche)}_{job_id[:8]}.csv")


def generate_job_csv_from_db(job_id: str, niche: str) -> Optional[str]:
    conn = get_db()
    rows = conn.execute(
        "SELECT data FROM leads WHERE job_id=? ORDER BY id ASC",
        (job_id,),
    ).fetchall()
    conn.close()

    records = []
    for row in rows:
        try:
            records.append(json.loads(row["data"]))
        except Exception:
            continue

    if not records:
        return None

    fieldnames = []
    seen_fields = set()
    for rec in records:
        for key in rec.keys():
            if key not in seen_fields:
                seen_fields.add(key)
                fieldnames.append(key)

    if not fieldnames:
        return None

    csv_path = build_job_csv_path(niche, job_id)
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    return csv_path


def _write_records_to_csv(records: list[dict], export_path: Path) -> Optional[str]:
    if not records:
        return None

    fieldnames = []
    seen_fields = set()
    for rec in records:
        for key in rec.keys():
            if key not in seen_fields:
                seen_fields.add(key)
                fieldnames.append(key)

    if not fieldnames:
        return None

    with open(export_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    return str(export_path)


def _collect_records_by_job_ids(job_ids: list[str], user_id: Optional[str] = None) -> list[dict]:
    if not job_ids:
        return []

    placeholders = ",".join("?" for _ in job_ids)
    sql = f"SELECT data FROM leads WHERE job_id IN ({placeholders})"
    params = list(job_ids)
    if user_id:
        sql += " AND user_id=?"
        params.append(user_id)
    sql += " ORDER BY id ASC"

    conn = get_db()
    rows = conn.execute(sql, tuple(params)).fetchall()
    conn.close()

    records = []
    for row in rows:
        try:
            records.append(json.loads(row["data"]))
        except Exception:
            continue
    return records


def generate_niche_csv_for_user(user_id: str, niche: str) -> Optional[str]:
    conn = get_db()
    job_rows = conn.execute(
        "SELECT job_id FROM jobs WHERE user_id=? AND niche=? ORDER BY created_at ASC",
        (user_id, niche),
    ).fetchall()
    conn.close()

    job_ids = [r["job_id"] for r in job_rows if r and r["job_id"]]
    records = _collect_records_by_job_ids(job_ids, user_id=user_id)
    export_path = OUTPUT_DIR / f"{_safe_slug(niche)}_{_safe_slug(user_id)}_combined.csv"
    return _write_records_to_csv(records, export_path)


def update_job_db(job_id: str, status: str, lead_count: Optional[int] = None, csv_path: Optional[str] = None):
    conn = get_db()
    if lead_count is None and csv_path is None:
        conn.execute("UPDATE jobs SET status=? WHERE job_id=?", (status, job_id))
    elif csv_path is None:
        conn.execute("UPDATE jobs SET status=?,lead_count=? WHERE job_id=?", (status, lead_count, job_id))
    else:
        conn.execute(
            "UPDATE jobs SET status=?,lead_count=?,csv_path=? WHERE job_id=?",
            (status, lead_count or 0, csv_path, job_id)
        )
    conn.commit()
    conn.close()


def publish_event(job: dict, message: dict):
    events = job.setdefault("events", [])
    events.append(message)
    if len(events) > EVENT_BUFFER_LIMIT:
        del events[: len(events) - EVENT_BUFFER_LIMIT]

    if message.get("type") == "lead":
        job["lead_count"] = int(job.get("lead_count", 0)) + 1

    dead_listeners = []
    for q in list(job.get("listeners", set())):
        try:
            q.put_nowait(message)
        except Exception:
            dead_listeners.append(q)

    for q in dead_listeners:
        job.get("listeners", set()).discard(q)


async def run_job(job_id: str):
    job = active_jobs.get(job_id)
    if not job:
        return

    profession = job["profession"]
    areas = job["areas"]
    user_id = job["user_id"]
    niche = job["niche"]

    conn = None
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from scraper_core import scrape_area_yields
        from utils import load_seen_leads, save_seen_leads, make_lead_key

        seen = load_seen_leads()
        total = len(areas)
        accepted_leads = 0
        completed_indexes = set()
        csv_path = build_job_csv_path(niche, job_id)
        pending_rows = []

        conn = get_db()
        conn.execute("UPDATE jobs SET csv_path=? WHERE job_id=?", (csv_path, job_id))
        conn.commit()
        job["total_areas"] = total

        def flush_pending(force_save_seen: bool = False):
            nonlocal accepted_leads, pending_rows
            if not pending_rows:
                return

            conn.executemany(
                "INSERT INTO leads (job_id,user_id,data) VALUES (?,?,?)",
                pending_rows,
            )
            accepted_leads += len(pending_rows)
            conn.execute("UPDATE jobs SET lead_count=? WHERE job_id=?", (accepted_leads, job_id))
            conn.commit()
            pending_rows = []

            if force_save_seen or accepted_leads % 300 == 0:
                save_seen_leads(seen)

        state_lock = asyncio.Lock()
        area_queue = asyncio.Queue()
        for i, area in enumerate(areas):
            area_queue.put_nowait((i, area))

        async def worker(worker_id: int):
            nonlocal completed_indexes
            while not job.get("cancelled"):
                try:
                    i, area = area_queue.get_nowait()
                except asyncio.QueueEmpty:
                    return

                query = f"{profession} in {area}"
                async with state_lock:
                    job["current_query"] = query
                    current_done = len(completed_indexes)

                publish_event(job, {
                    "type": "progress",
                    "data": {"current": current_done, "total": total, "query": query}
                })

                try:
                    async for lead in scrape_area_yields(query, profession):
                        if job.get("cancelled"):
                            break

                        lead["Search Query"] = query
                        should_publish = False
                        async with state_lock:
                            lead_key = make_lead_key(lead)
                            if lead_key not in seen:
                                seen.add(lead_key)
                                pending_rows.append((job_id, user_id, json.dumps(lead)))
                                if len(pending_rows) >= DB_FLUSH_EVERY:
                                    flush_pending()
                                should_publish = True

                        if should_publish:
                            publish_event(job, {"type": "lead", "data": lead})
                        await asyncio.sleep(0)
                finally:
                    async with state_lock:
                        completed_indexes.add(i)
                        processed_areas = len(completed_indexes)
                        job["processed_areas"] = processed_areas
                        flush_pending(force_save_seen=True)
                        conn.execute(
                            "UPDATE jobs SET processed_areas=?,completed_area_indexes=? WHERE job_id=?",
                            (processed_areas, json.dumps(sorted(completed_indexes)), job_id),
                        )
                        conn.commit()
                    area_queue.task_done()

        worker_count = min(AREA_CONCURRENCY, total) if total > 0 else 1
        workers = [asyncio.create_task(worker(i)) for i in range(worker_count)]
        await asyncio.gather(*workers, return_exceptions=True)

        flush_pending(force_save_seen=True)
        save_seen_leads(seen)

        final_status = "stopped" if job.get("cancelled") else "completed"

        generated = generate_job_csv_from_db(job_id, niche)
        # Keep a rolling combined export per niche so users can always fetch one complete file.
        generate_niche_csv_for_user(user_id, niche)
        update_job_db(job_id, final_status, accepted_leads, generated)
        job["status"] = final_status

        publish_event(job, {
            "type": "done",
            "data": {
                "total": accepted_leads,
                "status": final_status,
                "job_id": job_id,
            },
        })
    except Exception as e:
        job["status"] = "failed"
        update_job_db(job_id, "failed")
        publish_event(job, {"type": "error", "data": str(e)})
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
        job["finished_at"] = datetime.utcnow().isoformat()


def find_matching_running_job(user_id: str, profession: str, location: str, niche: str, areas_json: str):
    conn = get_db()
    rows = conn.execute(
        """
        SELECT job_id, status
        FROM jobs
        WHERE user_id=?
          AND profession=?
          AND location=?
          AND niche=?
                    AND areas=?
          AND status IN ('running','stopping')
        ORDER BY created_at DESC
        """,
                (user_id, profession, location, niche, areas_json),
    ).fetchall()
    conn.close()

    for row in rows:
        jid = row["job_id"]
        if jid in active_jobs and active_jobs[jid].get("status") in ("running", "stopping"):
            return jid

    # Clean stale rows where DB says running but worker is not active.
    if rows:
        conn = get_db()
        for row in rows:
            jid = row["job_id"]
            if jid not in active_jobs:
                conn.execute("UPDATE jobs SET status='stopped' WHERE job_id=?", (jid,))
        conn.commit()
        conn.close()

    return None


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            profession TEXT,
            location TEXT,
            niche TEXT,
            areas TEXT,
            status TEXT DEFAULT 'running',
            lead_count INTEGER DEFAULT 0,
            processed_areas INTEGER DEFAULT 0,
            completed_area_indexes TEXT,
            total_areas INTEGER DEFAULT 0,
            csv_path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(jobs)").fetchall()]
    if "processed_areas" not in cols:
        conn.execute("ALTER TABLE jobs ADD COLUMN processed_areas INTEGER DEFAULT 0")
    if "completed_area_indexes" not in cols:
        conn.execute("ALTER TABLE jobs ADD COLUMN completed_area_indexes TEXT")
    if "total_areas" not in cols:
        conn.execute("ALTER TABLE jobs ADD COLUMN total_areas INTEGER DEFAULT 0")
    if "root_job_id" not in cols:
        conn.execute("ALTER TABLE jobs ADD COLUMN root_job_id TEXT")
    if "resumed_from_job_id" not in cols:
        conn.execute("ALTER TABLE jobs ADD COLUMN resumed_from_job_id TEXT")
    conn.execute("UPDATE jobs SET root_job_id=job_id WHERE root_job_id IS NULL OR root_job_id='' ")
    conn.execute("UPDATE jobs SET completed_area_indexes='[]' WHERE completed_area_indexes IS NULL OR completed_area_indexes='' ")

    # If backend restarted, in-memory workers are gone; avoid stale "running" rows.
    conn.execute(
        "UPDATE jobs SET status='stopped' WHERE status IN ('running','stopping')"
    )

    admin_id = "admin_001"
    if not conn.execute("SELECT id FROM users WHERE id=?", (admin_id,)).fetchone():
        conn.execute(
            "INSERT INTO users (id,name,email,password_hash,role) VALUES (?,?,?,?,?)",
            (admin_id, "Admin", "admin@leadscout.com", hash_password("admin123"), "admin")
        )
    conn.commit()
    conn.close()


def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


init_db()


class RegisterBody(BaseModel):
    name: str
    email: str
    password: str


class LoginBody(BaseModel):
    email: str
    password: str


class ScrapeBody(BaseModel):
    profession: str
    areas: list[str]
    user_id: str
    niche: str
    location: Optional[str] = ""
    root_job_id: Optional[str] = None
    resumed_from_job_id: Optional[str] = None


class ResumeBody(BaseModel):
    user_id: str
    niche: Optional[str] = None
    restart_from_beginning: bool = False


@app.post("/auth/register")
def register(body: RegisterBody):
    conn = get_db()
    if conn.execute("SELECT id FROM users WHERE email=?", (body.email,)).fetchone():
        conn.close()
        raise HTTPException(400, "Email already registered")
    uid = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO users (id,name,email,password_hash,role) VALUES (?,?,?,?,?)",
        (uid, body.name, body.email, hash_password(body.password), "user")
    )
    conn.commit()
    conn.close()
    return {"user": {"id": uid, "name": body.name, "email": body.email, "role": "user"}}


@app.post("/auth/login")
def login(body: LoginBody):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password_hash=?",
        (body.email, hash_password(body.password))
    ).fetchone()
    conn.close()
    if not user:
        raise HTTPException(401, "Invalid email or password")
    return {"user": {
        "id": user["id"], "name": user["name"],
        "email": user["email"], "role": user["role"]
    }}


@app.post("/scrape/start")
async def start_scrape(body: ScrapeBody):
    job_id   = str(uuid.uuid4())
    location = body.location or (body.areas[0] if body.areas else "unknown")
    root_job_id = body.root_job_id or job_id
    conn = get_db()
    conn.execute(
        "INSERT INTO jobs (job_id,user_id,profession,location,niche,areas,status,processed_areas,completed_area_indexes,total_areas,root_job_id,resumed_from_job_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            job_id,
            body.user_id,
            body.profession,
            location,
            body.niche,
            json.dumps(body.areas),
            "running",
            0,
            "[]",
            len(body.areas),
            root_job_id,
            body.resumed_from_job_id,
        )
    )
    conn.commit()
    conn.close()
    active_jobs[job_id] = {
        "status": "running",
        "profession": body.profession,
        "areas": body.areas,
        "user_id": body.user_id,
        "niche": body.niche,
        "cancelled": False,
        "lead_count": 0,
        "processed_areas": 0,
        "total_areas": len(body.areas),
        "events": [],
        "listeners": set(),
        "finished_at": None,
        "current_query": "",
    }
    active_jobs[job_id]["task"] = asyncio.create_task(run_job(job_id))
    return {"job_id": job_id}


@app.post("/scrape/stop/{job_id}")
def stop_scrape(job_id: str):
    if job_id in active_jobs:
        active_jobs[job_id]["cancelled"] = True
        active_jobs[job_id]["status"] = "stopping"
    return {"ok": True}


@app.post("/scrape/resume/{job_id}")
async def resume_scrape(job_id: str, body: ResumeBody):
    conn = get_db()
    row = conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Job not found")

    if row["user_id"] != body.user_id:
        raise HTTPException(403, "You can only resume your own jobs")

    try:
        original_areas = json.loads(row["areas"] or "[]")
    except Exception:
        original_areas = []

    processed = int(row["processed_areas"] or 0)
    completed_indexes = set()
    try:
        completed_indexes = set(int(i) for i in json.loads(row["completed_area_indexes"] or "[]"))
    except Exception:
        completed_indexes = set()

    if body.restart_from_beginning:
        remaining = original_areas
    elif completed_indexes:
        remaining = [area for idx, area in enumerate(original_areas) if idx not in completed_indexes]
    else:
        # Backward compatibility for legacy jobs created before completed index tracking.
        remaining = original_areas[processed:]

    if not remaining:
        raise HTTPException(400, "No remaining areas to resume")

    target_niche = body.niche or row["niche"] or "resumed_scrape"
    target_location = remaining[0] if remaining else (row["location"] or "")
    target_areas_json = json.dumps(remaining)
    existing_job_id = find_matching_running_job(
        body.user_id,
        row["profession"] or "",
        target_location,
        target_niche,
        target_areas_json,
    )
    if existing_job_id:
        return {"job_id": existing_job_id, "reused": True}

    return await start_scrape(ScrapeBody(
        profession=row["profession"] or "",
        areas=remaining,
        user_id=body.user_id,
        niche=target_niche,
        location=target_location,
        root_job_id=row["root_job_id"] or row["job_id"],
        resumed_from_job_id=row["job_id"],
    ))


@app.get("/scrape/status/{job_id}")
def scrape_status(job_id: str):
    if job_id in active_jobs:
        job = active_jobs[job_id]
        return {
            "job_id": job_id,
            "status": job.get("status", "running"),
            "lead_count": int(job.get("lead_count", 0)),
            "processed_areas": int(job.get("processed_areas", 0)),
            "total_areas": int(job.get("total_areas", 0)),
            "current_query": job.get("current_query", ""),
            "running": job.get("status") in ("running", "stopping"),
        }

    conn = get_db()
    row = conn.execute(
        "SELECT job_id,status,lead_count,csv_path,processed_areas,total_areas FROM jobs WHERE job_id=?",
        (job_id,),
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Job not found")

    status = row["status"]
    if status in ("running", "stopping"):
        # DB row says running, but no active in-memory worker exists.
        status = "stopped"
        conn = get_db()
        conn.execute("UPDATE jobs SET status='stopped' WHERE job_id=?", (job_id,))
        conn.commit()
        conn.close()

    return {
        "job_id": row["job_id"],
        "status": status,
        "lead_count": row["lead_count"] or 0,
        "processed_areas": row["processed_areas"] or 0,
        "total_areas": row["total_areas"] or 0,
        "current_query": "",
        "running": False,
        "csv_path": row["csv_path"],
    }


@app.get("/scrape/download/{job_id}")
def download_csv(job_id: str):
    conn = get_db()
    job  = conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
    conn.close()
    if not job:
        raise HTTPException(404, "Job not found")

    csv_path = job["csv_path"]
    if not csv_path or not Path(csv_path).exists():
        generated = generate_job_csv_from_db(job_id, job["niche"] or "leads")
        if generated:
            csv_path = generated
            conn = get_db()
            conn.execute("UPDATE jobs SET csv_path=? WHERE job_id=?", (csv_path, job_id))
            conn.commit()
            conn.close()
        else:
            raise HTTPException(404, "CSV not ready yet")

    return FileResponse(csv_path, media_type="text/csv", filename=Path(csv_path).name)


@app.get("/scrape/download/all/{user_id}")
def download_all_csv(user_id: str):
    conn = get_db()
    job_rows = conn.execute(
        "SELECT job_id FROM jobs WHERE user_id=? ORDER BY created_at ASC",
        (user_id,),
    ).fetchall()
    conn.close()

    job_ids = [r["job_id"] for r in job_rows if r and r["job_id"]]
    records = _collect_records_by_job_ids(job_ids, user_id=user_id)

    if not records:
        raise HTTPException(404, "No scraped leads found for this user")

    export_path = OUTPUT_DIR / f"all_leads_{_safe_slug(user_id)}.csv"
    written = _write_records_to_csv(records, export_path)
    if not written:
        raise HTTPException(404, "No scraped leads found for this user")

    return FileResponse(str(export_path), media_type="text/csv", filename=export_path.name)


@app.get("/scrape/download/niche/{user_id}/{niche}")
def download_niche_csv(user_id: str, niche: str):
    path = generate_niche_csv_for_user(user_id, niche)
    if not path:
        raise HTTPException(404, "No scraped leads found for this niche")
    return FileResponse(path, media_type="text/csv", filename=Path(path).name)


@app.get("/scrape/download/merged/{user_id}")
def download_merged_job_ids_csv(user_id: str, job_ids: str):
    parsed_ids = [j.strip() for j in (job_ids or "").split(",") if j.strip()]
    if not parsed_ids:
        raise HTTPException(400, "No job_ids provided")

    conn = get_db()
    rows = conn.execute(
        f"SELECT job_id FROM jobs WHERE user_id=? AND job_id IN ({','.join('?' for _ in parsed_ids)})",
        tuple([user_id] + parsed_ids),
    ).fetchall()
    conn.close()

    allowed_ids = [r["job_id"] for r in rows if r and r["job_id"]]
    if not allowed_ids:
        raise HTTPException(404, "No matching jobs found")

    records = _collect_records_by_job_ids(allowed_ids, user_id=user_id)
    if not records:
        raise HTTPException(404, "No scraped leads found for selected jobs")

    merged_slug = _safe_slug("_".join(allowed_ids[:3]))
    export_path = OUTPUT_DIR / f"merged_{_safe_slug(user_id)}_{merged_slug}.csv"
    written = _write_records_to_csv(records, export_path)
    if not written:
        raise HTTPException(404, "No scraped leads found for selected jobs")

    return FileResponse(written, media_type="text/csv", filename=Path(written).name)


@app.websocket("/ws/{job_id}")
async def ws_scrape(ws: WebSocket, job_id: str):
    await ws.accept()

    if job_id not in active_jobs:
        await ws.send_json({"type": "error", "data": "Job not found"})
        await ws.close()
        return

    job = active_jobs[job_id]
    queue = asyncio.Queue(maxsize=WS_QUEUE_MAXSIZE)
    job.setdefault("listeners", set()).add(queue)

    try:
        # Replay buffered events so users can reconnect after page navigation.
        for evt in job.get("events", []):
            await ws.send_json(evt)

        while True:
            evt = await queue.get()
            await ws.send_json(evt)

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await ws.send_json({"type": "error", "data": str(e)})
        except:
            pass
    finally:
        job.get("listeners", set()).discard(queue)
        try:
            await ws.close()
        except:
            pass


@app.get("/user/history/{user_id}")
def user_history(user_id: str):
    conn = get_db()
    jobs = conn.execute(
        """
        SELECT
            j.*,
            COALESCE(l.persisted_leads, 0) AS persisted_leads,
            CASE
                WHEN COALESCE(l.persisted_leads, 0) > COALESCE(j.lead_count, 0)
                THEN COALESCE(l.persisted_leads, 0)
                ELSE COALESCE(j.lead_count, 0)
            END AS effective_lead_count
        FROM jobs j
        LEFT JOIN (
            SELECT job_id, COUNT(*) AS persisted_leads
            FROM leads
            GROUP BY job_id
        ) l ON l.job_id = j.job_id
        WHERE j.user_id=?
        ORDER BY j.created_at DESC
        LIMIT 50
        """,
        (user_id,)
    ).fetchall()
    conn.close()
    return {"history": [dict(j) for j in jobs]}


def require_admin(x_admin_key: str = Header(None)):
    conn = get_db()
    user = conn.execute("SELECT role FROM users WHERE id=?", (x_admin_key,)).fetchone()
    conn.close()
    if not user or user["role"] != "admin":
        raise HTTPException(403, "Admin access required")


@app.get("/admin/users")
def admin_users(x_admin_key: str = Header(None)):
    require_admin(x_admin_key)
    conn  = get_db()
    users = conn.execute("""
        SELECT
            u.*,
            COUNT(j.job_id) AS job_count,
            COALESCE(SUM(CASE
                WHEN COALESCE(l.persisted_leads, 0) > COALESCE(j.lead_count, 0)
                THEN COALESCE(l.persisted_leads, 0)
                ELSE COALESCE(j.lead_count, 0)
            END),0) AS total_leads
        FROM users u LEFT JOIN jobs j ON u.id=j.user_id
        LEFT JOIN (
            SELECT job_id, COUNT(*) AS persisted_leads
            FROM leads
            GROUP BY job_id
        ) l ON l.job_id = j.job_id
        GROUP BY u.id ORDER BY u.created_at DESC
    """).fetchall()
    conn.close()
    result = [dict(u) for u in users]
    for u in result:
        u.pop("password_hash", None)
    return {"users": result}


@app.get("/admin/jobs")
def admin_jobs(x_admin_key: str = Header(None)):
    require_admin(x_admin_key)
    conn = get_db()
    jobs = conn.execute("""
        SELECT
            j.*,
            u.name AS user_name,
            COALESCE(l.persisted_leads, 0) AS persisted_leads,
            CASE
                WHEN COALESCE(l.persisted_leads, 0) > COALESCE(j.lead_count, 0)
                THEN COALESCE(l.persisted_leads, 0)
                ELSE COALESCE(j.lead_count, 0)
            END AS effective_lead_count
        FROM jobs j
        LEFT JOIN users u ON j.user_id=u.id
        LEFT JOIN (
            SELECT job_id, COUNT(*) AS persisted_leads
            FROM leads
            GROUP BY job_id
        ) l ON l.job_id = j.job_id
        ORDER BY j.created_at DESC LIMIT 200
    """).fetchall()
    conn.close()
    return {"jobs": [dict(j) for j in jobs]}


@app.get("/admin/stats")
def admin_stats(x_admin_key: str = Header(None)):
    require_admin(x_admin_key)
    conn        = get_db()
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_jobs  = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    total_leads = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    top_pro     = conn.execute("SELECT profession,COUNT(*) as c FROM jobs GROUP BY profession ORDER BY c DESC LIMIT 1").fetchone()
    top_loc     = conn.execute("SELECT location,COUNT(*) as c FROM jobs GROUP BY location ORDER BY c DESC LIMIT 1").fetchone()
    avg_leads   = conn.execute("SELECT AVG(c) FROM (SELECT COUNT(*) AS c FROM leads GROUP BY job_id)").fetchone()[0]
    csv_files   = len(list(OUTPUT_DIR.glob("*.csv")))
    conn.close()
    return {
        "total_users":    total_users,
        "total_jobs":     total_jobs,
        "total_leads":    int(total_leads),
        "active_jobs":    sum(1 for j in active_jobs.values() if j.get("status") in ("running", "stopping")),
        "total_files":    csv_files,
        "top_profession": top_pro[0] if top_pro else None,
        "top_location":   top_loc[0] if top_loc else None,
        "avg_leads":      round(avg_leads) if avg_leads else 0,
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}