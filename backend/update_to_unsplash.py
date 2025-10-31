"""Update all activity images to use Unsplash instead of picsum.photos"""
from sqlalchemy import text
from app.database import SessionLocal

# Unsplash collections for different themes
THEMES = {
    'travel': '3330445',  # Travel & Places
    'nature': '1163637',  # Nature
    'landmarks': '3348849',  # Architecture & Landmarks
    'adventure': '1065976',  # Adventure
    'culture': '3356645',  # Arts & Culture
}

def main():
    db = SessionLocal()

    # Get all activities with their slugs
    activities = db.execute(text('''
        SELECT id, slug, title
        FROM activities
        ORDER BY id
    ''')).fetchall()

    print(f"Updating images for {len(activities)} activities...")

    for activity in activities:
        activity_id, slug, title = activity

        # Determine theme based on title keywords
        theme = 'travel'  # default
        title_lower = title.lower()
        if any(word in title_lower for word in ['museum', 'art', 'gallery', 'cathedral', 'palace']):
            theme = 'culture'
        elif any(word in title_lower for word in ['mountain', 'nature', 'park', 'beach', 'island']):
            theme = 'nature'
        elif any(word in title_lower for word in ['climb', 'hike', 'dive', 'adventure', 'safari']):
            theme = 'adventure'
        elif any(word in title_lower for word in ['tower', 'building', 'bridge', 'statue']):
            theme = 'landmarks'

        collection_id = THEMES[theme]

        # Update activity images
        images = db.execute(text('''
            SELECT id, is_primary
            FROM activity_images
            WHERE activity_id = :activity_id
            ORDER BY id
        '''), {'activity_id': activity_id}).fetchall()

        for idx, (image_id, is_primary) in enumerate(images):
            # Use Unsplash random from collection with unique seed
            url = f"https://source.unsplash.com/collection/{collection_id}/800x600?sig={slug}-{idx}"

            db.execute(text('''
                UPDATE activity_images
                SET url = :url
                WHERE id = :image_id
            '''), {'url': url, 'image_id': image_id})

        print(f"  Activity {activity_id} ({theme}): {len(images)} images updated")

    # Update destination images
    destinations = db.execute(text('SELECT id, slug FROM destinations')).fetchall()
    for dest_id, slug in destinations:
        url = f"https://source.unsplash.com/collection/3330445/1200x800?sig=dest-{slug}"
        db.execute(text('UPDATE destinations SET image_url = :url WHERE id = :id'),
                   {'url': url, 'id': dest_id})

    print(f"\nUpdated {len(destinations)} destination images")

    db.commit()
    print("\n✅ All images updated to Unsplash!")
    db.close()

if __name__ == '__main__':
    main()
