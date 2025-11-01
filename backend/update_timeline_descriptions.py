"""Update timeline descriptions with more detailed, realistic text."""

import random
from sqlalchemy import text
from app.database import SessionLocal
from app.models import ActivityTimeline


# Detailed stop descriptions based on activity types
STOP_DESCRIPTIONS = {
    "walking": [
        ("Historic City Center", "Begin your journey in the heart of the historic district. Your expert guide will introduce you to the area's rich history and point out architectural highlights. Learn about the founding of the city and how it evolved through the centuries."),
        ("Main Square", "Explore the bustling main square, the traditional meeting place for locals. Admire the stunning architecture surrounding the plaza and hear fascinating stories about the events that shaped this iconic space. Time for photos!"),
        ("Local Market", "Wander through the vibrant local market where residents shop for fresh produce, artisan goods, and traditional delicacies. Experience authentic local culture and maybe pick up some unique souvenirs. Your guide will recommend the best stalls."),
        ("Historic Monument", "Visit one of the city's most famous landmarks. Your guide will share the monument's fascinating history, architectural significance, and its role in shaping the local culture. Great opportunity for memorable photos."),
        ("Hidden Alleyways", "Discover charming hidden alleyways and secret spots that most tourists miss. Your guide will share local legends and point out unique architectural details. These quiet corners offer a glimpse into daily life away from the crowds."),
        ("Panoramic Viewpoint", "Reach a spectacular vantage point with breathtaking views over the city. Perfect for photography enthusiasts! Your guide will help you identify key landmarks and explain the city's layout and development."),
    ],
    "food": [
        ("First Tasting Stop", "Start your culinary adventure at a beloved local eatery. Sample authentic dishes that represent the region's culinary heritage. Your guide will explain the ingredients, preparation methods, and cultural significance of each dish."),
        ("Traditional Market Visit", "Explore a bustling food market filled with fresh, seasonal ingredients. Learn about local produce, spices, and specialty items. Watch vendors at work and discover ingredients you've never seen before."),
        ("Family-Run Restaurant", "Visit a family-owned establishment that has been serving traditional recipes for generations. Enjoy freshly prepared specialties and hear the stories behind the recipes passed down through the family."),
        ("Street Food Experience", "Discover the vibrant street food scene and taste popular local snacks. Learn why street food is such an important part of the local culture and which vendors the locals trust most."),
        ("Sweet Treats Stop", "Indulge in traditional desserts and pastries at a renowned bakery or café. Learn about the history of these sweet treats and how they're made using time-honored techniques."),
        ("Final Tasting", "Conclude your food tour at a special location where you'll sample signature dishes or beverages. Reflect on your culinary journey and get recommendations for where to eat during the rest of your stay."),
    ],
    "museum": [
        ("Museum Introduction", "Meet your expert guide and receive skip-the-line access. Get an overview of the museum's history, architecture, and most significant collections. Learn helpful tips for navigating the galleries efficiently."),
        ("Main Exhibition Hall", "Explore the museum's most famous permanent collection. Your guide will highlight masterpieces and share fascinating stories about the artists, historical context, and artistic movements represented."),
        ("Special Collection", "Discover a carefully curated special collection or temporary exhibition. Learn about the unique pieces on display and why they're significant to art history or the museum's holdings."),
        ("Hidden Gems", "Visit lesser-known galleries that many visitors miss. Your guide will show you unexpected treasures and share insider knowledge about the museum's lesser-celebrated but equally fascinating works."),
        ("Interactive Experience", "Engage with interactive displays or participate in hands-on activities. Perfect opportunity to deepen your understanding and create memorable moments. Great for all ages!"),
        ("Grand Finale", "Conclude your tour at the museum's most iconic space or artwork. Time for final questions, photos, and personal recommendations from your guide for further exploration."),
    ],
    "bus": [
        ("Downtown Route", "Begin your hop-on hop-off adventure through the city center. Pass by major landmarks, government buildings, and commercial districts. Informative audio commentary available in multiple languages provides historical context and interesting facts."),
        ("Historic District", "Travel through the charming old town with its narrow streets and centuries-old architecture. See preserved medieval buildings, historic churches, and traditional neighborhoods that showcase the city's heritage."),
        ("Waterfront & Parks", "Enjoy scenic views along the waterfront or through beautiful city parks. Perfect for photography! Learn about the city's relationship with water and how green spaces enhance urban life."),
        ("Cultural Quarter", "Discover the arts and culture district with museums, theaters, galleries, and performance venues. Pass by famous cultural institutions and learn about the city's vibrant artistic scene."),
        ("Modern District", "See contemporary architecture and modern developments. Contrast historic areas with cutting-edge buildings and urban planning. Understand how the city balances preservation with innovation."),
        ("Panoramic Views", "Route includes elevated roads or bridges offering spectacular panoramic city views. Ideal for capturing memorable photos and getting oriented with the city's layout and major landmarks."),
    ],
    "cruise": [
        ("Boarding & Departure", "Board your comfortable vessel and find your seat. As we depart, enjoy views of the shoreline and city skyline. Your guide will provide an overview of the route and points of interest you'll see."),
        ("Historic Waterfront", "Cruise past historic buildings and landmarks lining the waterfront. Learn about the area's maritime history and how the waterway shaped the city's development and economy."),
        ("Famous Bridges", "Pass under or alongside iconic bridges. Your guide will share fascinating engineering facts and historical stories about these architectural marvels that connect different parts of the city."),
        ("Scenic Highlights", "Enjoy the most picturesque sections of the route. Perfect for photography! See the city from unique vantage points that can only be experienced from the water."),
        ("Wildlife & Nature", "Look for local birds, aquatic life, and natural features along the waterway. Learn about the ecosystem and conservation efforts that protect this important natural corridor."),
        ("Return Journey", "Relax as we return to the starting point. Final opportunity for photos and questions. Your guide will provide recommendations for continuing your exploration of the waterfront area."),
    ]
}


def update_timelines():
    """Update existing timeline descriptions with more detailed text."""
    db = SessionLocal()

    try:
        # Get all activities with their titles
        activities = db.execute(text("""
            SELECT id, title, duration_minutes
            FROM activities
            ORDER BY id
        """)).fetchall()

        print(f"Updating timelines for {len(activities)} activities...")
        updated_count = 0

        for activity_id, title, duration in activities:
            # Determine activity type from title
            title_lower = title.lower()
            if "food" in title_lower or "culinary" in title_lower or "taste" in title_lower:
                stop_type = "food"
            elif "museum" in title_lower or "gallery" in title_lower or "skip-the-line" in title_lower:
                stop_type = "museum"
            elif "bus" in title_lower or "hop-on" in title_lower:
                stop_type = "bus"
            elif "cruise" in title_lower or "boat" in title_lower or "river" in title_lower:
                stop_type = "cruise"
            else:
                stop_type = "walking"

            # Get timelines for this activity
            timelines = db.query(ActivityTimeline).filter(
                ActivityTimeline.activity_id == activity_id
            ).order_by(ActivityTimeline.step_number).all()

            if not timelines:
                continue

            # Use activity-appropriate descriptions
            descriptions = STOP_DESCRIPTIONS.get(stop_type, STOP_DESCRIPTIONS["walking"])

            # Update each timeline with detailed description
            for idx, timeline in enumerate(timelines):
                # Use descriptions in order, or random if we run out
                if idx < len(descriptions):
                    stop_title, stop_desc = descriptions[idx]
                else:
                    stop_title, stop_desc = random.choice(descriptions)

                timeline.title = stop_title
                timeline.description = stop_desc
                updated_count += 1

        db.commit()
        print(f"\n✅ Successfully updated {updated_count} timeline descriptions!")

        # Show sample
        print("\nSample updated timeline:")
        sample = db.query(ActivityTimeline).first()
        if sample:
            print(f"  Title: {sample.title}")
            print(f"  Description: {sample.description[:150]}...")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    update_timelines()
