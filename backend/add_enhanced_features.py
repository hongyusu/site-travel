"""Add enhanced features to existing activities."""

import random
from decimal import Decimal
from sqlalchemy import text

from app.database import SessionLocal
from app.models import (
    Activity, ActivityTimeline, ActivityTimeSlot,
    ActivityPricingTier, ActivityAddOn
)


def add_enhanced_features():
    """Add timelines, time slots, pricing tiers, and add-ons to existing activities."""
    db = SessionLocal()

    try:
        # Get all activities
        activities = db.query(Activity).all()
        print(f"Found {len(activities)} activities")

        timeline_count = 0
        slot_count = 0
        tier_count = 0
        addon_count = 0

        for activity in activities:
            print(f"\nProcessing: {activity.title}")

            # Add timelines (What to Expect section)
            if activity.duration_minutes >= 60:
                num_stops = min(4, activity.duration_minutes // 30)
                stops = [
                    ("Historic landmark", "Visit the iconic monument"),
                    ("Local market", "Experience authentic local culture"),
                    ("Scenic viewpoint", "Take breathtaking photos"),
                    ("Traditional restaurant", "Enjoy local cuisine"),
                    ("Hidden gem", "Discover off-the-beaten-path location"),
                    ("Cultural site", "Learn about history and traditions")
                ]

                for i in range(num_stops):
                    stop_name, description = random.choice(stops)
                    duration = random.randint(30, 90)
                    timeline = ActivityTimeline(
                        activity_id=activity.id,
                        step_number=i + 1,
                        title=f"Stop {i+1}: {stop_name}",
                        description=description,
                        duration_minutes=duration
                    )
                    db.add(timeline)
                    timeline_count += 1

            # Add time slots
            time_options = [
                ("Morning", "09:00", 0),
                ("Late Morning", "11:00", Decimal("5.00")),
                ("Afternoon", "14:00", Decimal("10.00")),
                ("Late Afternoon", "16:00", Decimal("5.00")),
                ("Evening", "18:00", Decimal("15.00"))
            ]

            for label, time, adj in time_options[:4]:
                slot = ActivityTimeSlot(
                    activity_id=activity.id,
                    slot_label=label,
                    slot_time=time,
                    price_adjustment=adj,
                    max_capacity=random.randint(10, 30)
                )
                db.add(slot)
                slot_count += 1

            # Add pricing tiers
            base_price = float(activity.price_adult)
            tiers = [
                ("Standard", 0, 0),
                ("Premium", 0.3, 0.3),
                ("VIP", 0.5, 0.5)
            ]

            for tier_name, adult_mult, child_mult in tiers:
                tier = ActivityPricingTier(
                    activity_id=activity.id,
                    tier_name=tier_name,
                    price_adult=Decimal(str(base_price * (1 + adult_mult))),
                    price_child=Decimal(str(float(activity.price_child or 0) * (1 + child_mult))) if activity.price_child else None,
                    tier_description=f"{tier_name} experience with additional benefits"
                )
                db.add(tier)
                tier_count += 1

            # Add add-ons
            addons_options = [
                ("Professional Photos", Decimal("25.00"), True),
                ("Lunch Package", Decimal("35.00"), True),
                ("Private Guide", Decimal("50.00"), True),
                ("Audio Guide", Decimal("10.00"), False)
            ]

            for addon_name, price, optional in random.sample(addons_options, min(3, len(addons_options))):
                addon = ActivityAddOn(
                    activity_id=activity.id,
                    name=addon_name,
                    description=f"Enhance your experience with {addon_name.lower()}",
                    price=price,
                    is_optional=optional
                )
                db.add(addon)
                addon_count += 1

        db.commit()
        print(f"\n✅ Enhanced features added successfully!")
        print(f"   Timelines: {timeline_count}")
        print(f"   Time Slots: {slot_count}")
        print(f"   Pricing Tiers: {tier_count}")
        print(f"   Add-ons: {addon_count}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_enhanced_features()
