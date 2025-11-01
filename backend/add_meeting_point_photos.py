"""Add photos to meeting points."""

import random
from sqlalchemy import text
from app.database import SessionLocal
from app.models import MeetingPoint, MeetingPointPhoto


def add_meeting_point_photos():
    """Add 2-4 photos to each meeting point."""
    db = SessionLocal()

    try:
        # Get all meeting points
        meeting_points = db.query(MeetingPoint).all()
        print(f"Found {len(meeting_points)} meeting points")

        photo_count = 0

        for mp in meeting_points:
            # Add 2-4 photos per meeting point
            num_photos = random.randint(2, 4)

            for i in range(num_photos):
                # Use picsum.photos with seed for consistent images
                photo_url = f"https://picsum.photos/seed/meeting-{mp.id}-{i}/800/600"

                photo = MeetingPointPhoto(
                    meeting_point_id=mp.id,
                    url=photo_url,
                    caption=f"Meeting point view {i+1}",
                    order_index=i
                )
                db.add(photo)
                photo_count += 1

        db.commit()
        print(f"\n✅ Successfully added {photo_count} meeting point photos!")

        # Show sample
        print("\nSample meeting point with photos:")
        first_mp = meeting_points[0]
        photos = db.query(MeetingPointPhoto).filter(
            MeetingPointPhoto.meeting_point_id == first_mp.id
        ).all()
        print(f"  Meeting Point: {first_mp.name}")
        print(f"  Photos: {len(photos)}")
        for photo in photos:
            print(f"    - {photo.url}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_meeting_point_photos()
