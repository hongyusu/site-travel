"""Update image URLs to use placehold.co."""

from sqlalchemy import text
from app.database import SessionLocal

def update_images():
    """Update all image URLs in the database."""
    db = SessionLocal()
    
    try:
        # Update destination images with colorful placeholders
        destinations = db.execute(text("SELECT id, name FROM destinations")).fetchall()
        for dest_id, name in destinations:
            # Use a hash of the name to get consistent color
            color_hash = hash(name) % 16
            colors = ['FF6B6B', 'FFA500', 'FFD700', '4ECDC4', '45B7D1', '96CEB4', 
                     'FFEAA7', 'DFE6E9', 'B8E6B8', 'FFB6C1', 'C7CEEA', 'FF9FF3']
            color = colors[color_hash % len(colors)]
            
            db.execute(text(
                "UPDATE destinations SET image_url = :url WHERE id = :id"
            ), {"url": f"https://placehold.co/800x600/{color}/FFF?text={name.replace(' ', '+')}", "id": dest_id})
        
        # Update activity images
        activities = db.execute(text("SELECT id, title FROM activities")).fetchall()
        for act_id, title in activities:
            color_hash = hash(title) % 16
            colors = ['FF6B6B', 'FFA500', 'FFD700', '4ECDC4', '45B7D1', '96CEB4', 
                     'FFEAA7', 'DFE6E9', 'B8E6B8', 'FFB6C1', 'C7CEEA', 'FF9FF3']
            
            for i in range(3):
                color = colors[(color_hash + i) % len(colors)]
                db.execute(text("""
                    UPDATE activity_images 
                    SET url = :url 
                    WHERE activity_id = :act_id AND order_index = :idx
                """), {
                    "url": f"https://placehold.co/800x600/{color}/FFF?text=Activity+{i+1}",
                    "act_id": act_id,
                    "idx": i
                })
        
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
