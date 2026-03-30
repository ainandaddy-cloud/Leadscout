"""
scraper_core.py
Launches standalone_scraper.py using subprocess.Popen (not asyncio).
Uses a thread to read output without blocking FastAPI.
This works on Windows + Python 3.13 + FastAPI.
"""

import asyncio
import json
import os
import sys
import subprocess
import threading
import queue
from pathlib import Path

STANDALONE = str(Path(__file__).parent / "standalone_scraper.py")
PYTHON     = sys.executable
try:
    POLL_SLEEP = max(0.005, min(0.05, float(os.getenv("LEADSCOUT_SUBPROCESS_POLL_SLEEP", "0.03"))))
except ValueError:
    POLL_SLEEP = 0.03


async def scrape_area_yields(query: str, profession: str):
    """
    Async generator — launches standalone_scraper.py via subprocess.Popen.
    Reads output in a background thread and yields typed events.
    Event shape: {"type": "lead|info|count|blocked|error|done", "data": any}
    """
    result_queue = queue.Queue()

    def read_output(proc, q):
        """Reads subprocess stdout in a background thread."""
        try:
            for line in proc.stdout:
                line = line.strip()
                if line:
                    q.put(line)
        except Exception as e:
            q.put(json.dumps({"type": "error", "data": str(e)}))
        finally:
            q.put(None)  # Signal done

    # Launch standalone scraper as a regular subprocess
    try:
        proc = subprocess.Popen(
            [PYTHON, STANDALONE, query, profession, "job"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore",
            bufsize=1,
        )
    except Exception as e:
        return

    # Start background thread to read output
    thread = threading.Thread(target=read_output, args=(proc, result_queue), daemon=True)
    thread.start()

    # Yield results as they arrive
    while True:
        try:
            line = result_queue.get_nowait()
        except queue.Empty:
            await asyncio.sleep(POLL_SLEEP)
            continue

        if line is None:
            break

        try:
            msg = json.loads(line)
            msg_type = msg.get("type")
            if msg_type in ("lead", "info", "count", "blocked", "error", "done"):
                yield msg
            if msg_type in ("done", "error", "blocked"):
                break
        except json.JSONDecodeError:
            continue

    # Cleanup
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except:
            pass