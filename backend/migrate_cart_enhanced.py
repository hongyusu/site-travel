"""Add enhanced booking fields to cart_items table."""

from sqlalchemy import text
from app.database import engine, SessionLocal


def migrate():
    """Add enhanced booking columns to cart_items table."""
    print("Starting cart_items table migration...")

    db = SessionLocal()

    try:
        # Add enhanced booking fields to cart_items table
        migrations = [
            "ALTER TABLE cart_items ADD COLUMN IF NOT EXISTS time_slot_id INTEGER REFERENCES activity_time_slots(id) ON DELETE SET NULL",
            "ALTER TABLE cart_items ADD COLUMN IF NOT EXISTS pricing_tier_id INTEGER REFERENCES activity_pricing_tiers(id) ON DELETE SET NULL",
            "ALTER TABLE cart_items ADD COLUMN IF NOT EXISTS add_on_ids TEXT",
            "ALTER TABLE cart_items ADD COLUMN IF NOT EXISTS add_on_quantities TEXT"
        ]

        for migration_sql in migrations:
            print(f"Executing: {migration_sql}")
            db.execute(text(migration_sql))

        db.commit()
        print("✅ Migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate()
