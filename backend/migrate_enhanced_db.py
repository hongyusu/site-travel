"""
Enhanced database migration script.
This script drops the existing database and recreates it with all new tables and fields.
"""

from app.database import Base, engine
from app.models import *  # Import all models

def migrate_database():
    """Drop all tables and recreate with new schema."""
    print("🗑️  Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped")

    print("\n🔨 Creating all tables with enhanced schema...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created with new fields")

    print("\n📋 New tables created:")
    print("   - activities (with 18+ new columns)")
    print("   - activity_timelines (new)")
    print("   - activity_time_slots (new)")
    print("   - activity_pricing_tiers (new)")
    print("   - activity_add_ons (new)")
    print("   - meeting_point_photos (new)")
    print("   - review_categories (new)")
    print("   - activity_images (updated with caption, is_hero)")
    print("   - meeting_points (updated with parking, transport info)")

    print("\n✨ Database migration complete!")
    print("⚠️  Note: All existing data has been removed")
    print("📝 Run seed script next to populate with enhanced data")

if __name__ == "__main__":
    migrate_database()
