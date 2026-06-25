#!/usr/bin/env python3
"""Set meeting-point coordinates for Finuo-Giraffe activities from the departure city.

Girafe meeting points have no precise coordinates, so the map showed "map not
available". This sets each activity's meeting_point lat/lng to its departure
city's coordinates (from girafe_meeting_coords.json), so the map renders. In place.

    docker exec travel_backend python /app/apply_girafe_meeting_coords.py
"""
import json, os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.models.activity import Activity, MeetingPoint

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    coords = json.load(open(os.path.join(here, "girafe_meeting_coords.json"), encoding="utf-8"))
    s = Session()
    try:
        n = 0
        for slug, c in coords.items():
            act = s.query(Activity).filter_by(slug=slug).first()
            if not act:
                continue
            for mp in s.query(MeetingPoint).filter_by(activity_id=act.id).all():
                mp.latitude = c["lat"]; mp.longitude = c["lng"]; n += 1
        s.commit()
        print(f"Set meeting-point coordinates on {n} activities.")
    except Exception as e:
        s.rollback(); print("ERROR:", e); raise
    finally:
        s.close()


if __name__ == "__main__":
    run()
