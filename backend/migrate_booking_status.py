"""Add enhanced booking status and vendor management fields to bookings table."""

from sqlalchemy import text
from app.database import engine, SessionLocal


def migrate():
    """Add new booking statuses and vendor management columns."""
    print("Starting booking status migration...")

    db = SessionLocal()

    try:
        # Add new enum values to bookingstatus type
        migrations = [
            "ALTER TYPE bookingstatus ADD VALUE IF NOT EXISTS 'pending_vendor_approval'",
            "ALTER TYPE bookingstatus ADD VALUE IF NOT EXISTS 'rejected'",

            # Add vendor management columns
            "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS rejection_reason TEXT",
            "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS vendor_approved_at TIMESTAMP WITH TIME ZONE",
            "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS vendor_rejected_at TIMESTAMP WITH TIME ZONE"
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
