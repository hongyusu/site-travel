"""Update image URLs from Unsplash to Picsum."""

from sqlalchemy import text
from app.database import SessionLocal

def update_images():
    """Update all image URLs in the database."""
    db = SessionLocal()
    
    try:
        # Update destination images
        db.execute(text("""
            UPDATE destinations 
            SET image_url = CONCAT('https://picsum.photos/seed/', slug, '/800/600')
            WHERE image_url LIKE '%unsplash%'
        """))
        
        # Update activity images
        db.execute(text("""
            UPDATE activity_images
            SET url = CONCAT('https://picsum.photos/seed/', 
                (SELECT slug FROM activities WHERE id = activity_images.activity_id),
                '-', order_index, '/800/600')
            WHERE url LIKE '%unsplash%'
        """))
        
        db.commit()
        print("Image URLs updated successfully!")
        
    except Exception as e:
        print(f"Error updating images: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_images()
