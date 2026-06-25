#!/usr/bin/env python3
"""Apply rich per-day subsections (Girafe layout) to Finuo-Giraffe timelines.

Adds the activity_timelines.sections JSONB column if missing, then for each
slug in girafe_sections.json sets each timeline row's `sections` (keyed by
step_number) to the bilingual {overview, accommodation, highlights,
attractions[]} structure. In place — touches only the sections column.

    docker exec travel_backend python /app/apply_girafe_sections.py
"""
import json, os, sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.models.activity import Activity, ActivityTimeline

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(os.path.join(here, "girafe_sections.json"), encoding="utf-8"))
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE activity_timelines ADD COLUMN IF NOT EXISTS sections JSONB"))
    s = Session()
    try:
        rows = 0; tours = 0
        for slug, days in data.items():
            act = s.query(Activity).filter_by(slug=slug).first()
            if not act:
                print("  ? missing", slug); continue
            tours += 1
            for tl in s.query(ActivityTimeline).filter_by(activity_id=act.id).all():
                sec = days.get(str(tl.step_number))
                if sec:
                    tl.sections = sec; rows += 1
        s.commit()
        print(f"Set sections on {rows} timeline rows across {tours} tours.")
    except Exception as e:
        s.rollback(); print("ERROR:", e); raise
    finally:
        s.close()


if __name__ == "__main__":
    run()
