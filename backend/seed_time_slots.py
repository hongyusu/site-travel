#!/usr/bin/env python3
"""
Seed time slots for activities that currently have none.

Run via Docker:
    docker run --rm --network site-travel_app-network \
        -v $(pwd)/backend:/app -w /app \
        -e DATABASE_URL=postgresql://postgres:password@findtravelmate_db:5432/findtravelmate \
        python:3.12-slim bash -c "pip install -q sqlalchemy psycopg2-binary 2>/dev/null && python seed_time_slots.py"
"""

import os
import sys
from decimal import Decimal

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import Base
from app.models.activity import Activity, ActivityTimeSlot

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/findtravelmate",
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

TIME_SLOTS = [
    {"slot_time": "09:00", "slot_label": "Morning", "price_adjustment": Decimal("0.00")},
    {"slot_time": "13:00", "slot_label": "Afternoon", "price_adjustment": Decimal("0.00")},
    {"slot_time": "17:00", "slot_label": "Evening", "price_adjustment": Decimal("5.00")},
]


def fix_sequence(session):
    """Fix the activity_time_slots id sequence to avoid conflicts."""
    session.execute(
        text(
            "SELECT setval("
            "pg_get_serial_sequence('activity_time_slots', 'id'), "
            "COALESCE((SELECT MAX(id) FROM activity_time_slots), 0) + 1, "
            "false)"
        )
    )
    session.commit()
    print("Fixed activity_time_slots id sequence.")


def seed_time_slots():
    session = Session()
    try:
        fix_sequence(session)

        # Find activities with no time slots
        activities_without_slots = (
            session.query(Activity)
            .filter(~Activity.id.in_(
                session.query(ActivityTimeSlot.activity_id).distinct()
            ))
            .order_by(Activity.id)
            .all()
        )

        if not activities_without_slots:
            print("All activities already have time slots. Nothing to do.")
            return

        print(f"Found {len(activities_without_slots)} activities without time slots.")

        total_added = 0
        for activity in activities_without_slots:
            capacity = activity.max_group_size or 20  # fallback
            for slot in TIME_SLOTS:
                ts = ActivityTimeSlot(
                    activity_id=activity.id,
                    slot_time=slot["slot_time"],
                    slot_label=slot["slot_label"],
                    max_capacity=capacity,
                    is_available=True,
                    price_adjustment=slot["price_adjustment"],
                )
                session.add(ts)
                total_added += 1
            print(f"  Added 3 time slots for activity {activity.id}: {activity.title}")

        session.commit()
        print(f"\nDone. Added {total_added} time slots for {len(activities_without_slots)} activities.")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_time_slots()
