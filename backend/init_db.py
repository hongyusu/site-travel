#!/usr/bin/env python3
"""
Initialize database schema using SQLAlchemy models.
Called by docker-entrypoint.sh when AUTO_INIT_DB=true and DB is empty.

This only creates tables — it does NOT seed demo data.
To load demo data, restore from a backup:
    psql -U postgres -d findtravelmate < /backups/backup_2026-04-14_expanded.sql
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, engine

# Import all models so Base.metadata knows about them
from app.models.user import User, Vendor  # noqa: F401
from app.models.activity import (  # noqa: F401
    Category, Destination, Activity, ActivityImage, ActivityCategory,
    ActivityDestination, ActivityHighlight, ActivityInclude, ActivityFAQ,
    MeetingPoint, ActivityTimeline, ActivityTimeSlot, ActivityPricingTier,
    ActivityAddOn, MeetingPointPhoto,
)
from app.models.booking import Booking, Availability, CartItem  # noqa: F401
from app.models.review import Review, ReviewImage, ReviewCategory  # noqa: F401
from app.models.wishlist import Wishlist  # noqa: F401
from app.models.translation import (  # noqa: F401
    ActivityTranslation, ActivityHighlightTranslation,
    ActivityIncludeTranslation, ActivityFAQTranslation,
    ActivityTimelineTranslation, ActivityPricingTierTranslation,
    ActivityAddOnTranslation, MeetingPointTranslation,
    CategoryTranslation, DestinationTranslation,
)


def main():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done. Tables created successfully.")
    print("To load demo data, restore from backup:")
    print("  psql -U postgres -d findtravelmate < /backups/backup_2026-04-14_expanded.sql")


if __name__ == "__main__":
    main()
