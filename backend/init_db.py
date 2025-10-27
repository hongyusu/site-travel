"""Initialize database and create demo data."""

import random
from datetime import datetime, date, timedelta
from decimal import Decimal
from slugify import slugify

from app.database import SessionLocal, engine, Base
from app.models import (
    User, Vendor, Category, Destination, Activity,
    ActivityImage, ActivityCategory, ActivityDestination,
    ActivityHighlight, ActivityInclude, MeetingPoint
)
from app.models.user import UserRole
from app.core.security import get_password_hash


def init_db():
    """Initialize database with tables and demo data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")

    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already contains data. Skipping initialization.")
            return

        print("Creating demo data...")

        # Create admin user
        admin = User(
            email="admin@getyourguide.com",
            password_hash=get_password_hash("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            email_verified=True
        )
        db.add(admin)

        # Create test customer
        customer = User(
            email="customer@example.com",
            password_hash=get_password_hash("customer123"),
            full_name="John Doe",
            role=UserRole.CUSTOMER,
            email_verified=True
        )
        db.add(customer)

        # Create test vendors
        vendor_users = []
        vendor_profiles = []

        vendor_data = [
            ("City Explorer Tours", "Premium city tours and experiences"),
            ("Local Flavors", "Authentic food and culinary experiences"),
            ("Adventure Seekers", "Outdoor and adventure activities"),
            ("Cultural Connections", "Museums, history, and cultural tours"),
            ("VIP Experiences", "Luxury and exclusive tours")
        ]

        for i, (company_name, description) in enumerate(vendor_data, 1):
            vendor_user = User(
                email=f"vendor{i}@example.com",
                password_hash=get_password_hash("vendor123"),
                full_name=f"{company_name} Manager",
                role=UserRole.VENDOR,
                email_verified=True
            )
            vendor_users.append(vendor_user)
            db.add(vendor_user)
            db.flush()

            vendor_profile = Vendor(
                user_id=vendor_user.id,
                company_name=company_name,
                description=description,
                is_verified=True,
                commission_rate=20.0
            )
            vendor_profiles.append(vendor_profile)
            db.add(vendor_profile)

        # Create categories
        categories = []
        category_data = [
            ("Tours & Sightseeing", "tours-sightseeing", "🏛️"),
            ("Museums & Attractions", "museums-attractions", "🎨"),
            ("Day Trips", "day-trips", "🚌"),
            ("Food & Drink", "food-drink", "🍽️"),
            ("Adventure & Nature", "adventure-nature", "🏔️"),
            ("Shows & Entertainment", "shows-entertainment", "🎭"),
            ("Transportation", "transportation", "🚗"),
            ("Water Sports", "water-sports", "🏄")
        ]

        for name, slug, icon in category_data:
            category = Category(name=name, slug=slug, icon=icon)
            categories.append(category)
            db.add(category)

        # Create destinations
        destinations = []
        destination_data = [
            ("Paris", "France", "FR", 48.8566, 2.3522),
            ("London", "United Kingdom", "GB", 51.5074, -0.1278),
            ("New York", "United States", "US", 40.7128, -74.0060),
            ("Rome", "Italy", "IT", 41.9028, 12.4964),
            ("Tokyo", "Japan", "JP", 35.6762, 139.6503),
            ("Barcelona", "Spain", "ES", 41.3851, 2.1734),
            ("Dubai", "United Arab Emirates", "AE", 25.2048, 55.2708),
            ("Amsterdam", "Netherlands", "NL", 52.3676, 4.9041),
            ("Prague", "Czech Republic", "CZ", 50.0755, 14.4378),
            ("Istanbul", "Turkey", "TR", 41.0082, 28.9784)
        ]

        for name, country, code, lat, lng in destination_data:
            destination = Destination(
                name=name,
                slug=slugify(name),
                country=country,
                country_code=code,
                latitude=lat,
                longitude=lng,
                is_featured=True,
                image_url=f"https://source.unsplash.com/800x600/?{name},city"
            )
            destinations.append(destination)
            db.add(destination)

        db.flush()

        # Create sample activities
        activity_templates = [
            {
                "title": "{city} City Walking Tour",
                "description": "Explore the historic heart of {city} on this comprehensive walking tour.",
                "price": 25,
                "duration": 180,
                "category": 0,  # Tours
            },
            {
                "title": "{city} Food Tour",
                "description": "Taste the best local cuisine and learn about {city}'s culinary traditions.",
                "price": 65,
                "duration": 240,
                "category": 3,  # Food & Drink
            },
            {
                "title": "Skip-the-Line: {city} Museum Pass",
                "description": "Access major museums in {city} without waiting in long queues.",
                "price": 45,
                "duration": 480,
                "category": 1,  # Museums
                "skip_the_line": True
            },
            {
                "title": "{city} Hop-On Hop-Off Bus Tour",
                "description": "See all of {city}'s major attractions at your own pace.",
                "price": 35,
                "duration": 1440,
                "category": 0,  # Tours
            },
            {
                "title": "{city} River Cruise",
                "description": "Enjoy stunning views of {city} from the water.",
                "price": 30,
                "duration": 90,
                "category": 0,  # Tours
            }
        ]

        activities_created = 0
        for destination in destinations[:5]:  # Create activities for first 5 cities
            for template in activity_templates:
                vendor = random.choice(vendor_profiles)

                title = template["title"].replace("{city}", destination.name)
                activity = Activity(
                    vendor_id=vendor.id,
                    title=title,
                    slug=slugify(title),
                    description=template["description"].replace("{city}", destination.name),
                    short_description=f"Experience the best of {destination.name}",
                    price_adult=Decimal(str(template["price"] + random.randint(-10, 20))),
                    price_child=Decimal(str(template["price"] * 0.5)),
                    duration_minutes=template["duration"],
                    max_group_size=random.randint(10, 30),
                    instant_confirmation=True,
                    free_cancellation_hours=24,
                    languages=["English", "Spanish", "French"],
                    is_bestseller=random.choice([True, False, False]),
                    is_skip_the_line=template.get("skip_the_line", False),
                    average_rating=round(random.uniform(4.0, 5.0), 1),
                    total_reviews=random.randint(50, 500),
                    total_bookings=random.randint(100, 1000)
                )
                db.add(activity)
                db.flush()

                # Add images
                for i in range(3):
                    image = ActivityImage(
                        activity_id=activity.id,
                        url=f"https://source.unsplash.com/800x600/?{destination.name},{template['category']}",
                        is_primary=(i == 0),
                        order_index=i
                    )
                    db.add(image)

                # Add category
                activity_category = ActivityCategory(
                    activity_id=activity.id,
                    category_id=categories[template["category"]].id
                )
                db.add(activity_category)

                # Add destination
                activity_destination = ActivityDestination(
                    activity_id=activity.id,
                    destination_id=destination.id
                )
                db.add(activity_destination)

                # Add highlights
                highlights = [
                    f"Professional guide",
                    f"Small group tour",
                    f"Free cancellation",
                    f"{destination.name} highlights"
                ]
                for i, text in enumerate(highlights):
                    highlight = ActivityHighlight(
                        activity_id=activity.id,
                        text=text,
                        order_index=i
                    )
                    db.add(highlight)

                # Add includes
                includes_data = [
                    ("Professional guide", True),
                    ("Transportation", random.choice([True, False])),
                    ("Entrance fees", True),
                    ("Food and drinks", False),
                    ("Hotel pickup", False)
                ]
                for i, (item, is_included) in enumerate(includes_data):
                    include = ActivityInclude(
                        activity_id=activity.id,
                        item=item,
                        is_included=is_included,
                        order_index=i
                    )
                    db.add(include)

                # Add meeting point
                meeting_point = MeetingPoint(
                    activity_id=activity.id,
                    address=f"Main Square, {destination.name} City Center",
                    instructions="Meet at the fountain in the center of the square",
                    latitude=destination.latitude + random.uniform(-0.01, 0.01),
                    longitude=destination.longitude + random.uniform(-0.01, 0.01)
                )
                db.add(meeting_point)

                activities_created += 1

        db.commit()
        print(f"Demo data created successfully!")
        print(f"- 1 Admin user (admin@getyourguide.com / admin123)")
        print(f"- 1 Customer (customer@example.com / customer123)")
        print(f"- {len(vendor_users)} Vendors (vendor1-5@example.com / vendor123)")
        print(f"- {len(categories)} Categories")
        print(f"- {len(destinations)} Destinations")
        print(f"- {activities_created} Activities")

    except Exception as e:
        print(f"Error creating demo data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()