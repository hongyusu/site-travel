"""Update activity images with more realistic placeholders from Picsum."""

from sqlalchemy import text
from app.database import SessionLocal

def update_images():
    db = SessionLocal()

    try:
        # Get all activities
        activities = db.execute(text("SELECT id, title FROM activities ORDER BY id")).fetchall()

        # Picsum provides realistic photo placeholders
        # We'll use different seed values to get different images
        base_url = "https://picsum.photos/seed"

        image_id = 1
        for activity in activities:
            activity_id = activity[0]
            activity_title = activity[1]

            # Generate 3 different images per activity
            for i in range(3):
                seed = f"activity{activity_id}-{i}"
                url = f"{base_url}/{seed}/800/600"
                is_primary = (i == 0)

                # Update the image URL
                db.execute(text(f"""
                    UPDATE activity_images
                    SET url = :url
                    WHERE id = :image_id
                """), {"url": url, "image_id": image_id})

                print(f"Updated image {image_id} for activity {activity_id} ({activity_title}): {url}")
                image_id += 1

        # Update destination images as well
        destinations = db.execute(text("SELECT id, name FROM destinations ORDER BY id")).fetchall()

        for dest in destinations:
            dest_id = dest[0]
            dest_name = dest[1]
            seed = f"destination{dest_id}"
            url = f"{base_url}/{seed}/1200/600"

            db.execute(text("""
                UPDATE destinations
                SET image_url = :url
                WHERE id = :dest_id
            """), {"url": url, "dest_id": dest_id})

            print(f"Updated destination {dest_id} ({dest_name}): {url}")

        db.commit()
        print("\n✓ Successfully updated all images with realistic placeholders!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_images()
