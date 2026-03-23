import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("leadscout.db")


def parse_json_list(value):
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except Exception:
        return []
    if isinstance(parsed, list):
        return parsed
    return []


def main():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT
            job_id,
            status,
            areas,
            completed_area_indexes,
            processed_areas,
            created_at
        FROM jobs
        WHERE lower(niche) LIKE '%bangalore%'
        ORDER BY created_at
        """
    ).fetchall()

    planned = set()
    scraped = set()

    for job_id, status, areas_raw, done_idx_raw, processed_areas, created_at in rows:
        areas = [str(x).strip() for x in parse_json_list(areas_raw) if str(x).strip()]
        for area in areas:
            planned.add(area)

        done_indexes = parse_json_list(done_idx_raw)

        if status == "completed" and areas:
            done_areas = areas
        elif done_indexes:
            done_areas = [
                areas[i]
                for i in done_indexes
                if isinstance(i, int) and 0 <= i < len(areas)
            ]
        else:
            n = int(processed_areas or 0)
            n = max(0, min(n, len(areas)))
            done_areas = areas[:n]

        for area in done_areas:
            scraped.add(area)

    missing = sorted(planned - scraped)
    scraped_sorted = sorted(scraped)

    print(f"BANGALORE_JOBS={len(rows)}")
    print(f"PLANNED_UNIQUE={len(planned)}")
    print(f"SCRAPED_UNIQUE={len(scraped_sorted)}")
    print(f"MISSING_UNIQUE={len(missing)}")
    print("SCRAPED_PLACES_START")
    for area in scraped_sorted:
        print(area)
    print("SCRAPED_PLACES_END")
    print("MISSING_PLACES_START")
    for area in missing:
        print(area)
    print("MISSING_PLACES_END")

    conn.close()


if __name__ == "__main__":
    main()
