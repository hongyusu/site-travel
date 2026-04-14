#!/usr/bin/env python3
"""
Seed reviews for activities that currently have no reviews.

Run via Docker:
    docker run --rm --network site-travel_app-network \
        -v $(pwd)/backend:/app -w /app \
        -e DATABASE_URL=postgresql://postgres:password@findtravelmate_db:5432/findtravelmate \
        python:3.12-slim bash -c "pip install -q sqlalchemy psycopg2-binary && python seed_reviews.py"
"""

import os
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/findtravelmate",
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Review templates: (title, comment_template)
# {activity} will be replaced with the activity title at insertion time.
REVIEW_TEMPLATES = [
    (
        "Unforgettable experience",
        "This was the highlight of our trip! The guide was incredibly knowledgeable "
        "and passionate. Every moment felt carefully planned yet spontaneous. "
        "Would recommend to anyone visiting the area.",
    ),
    (
        "Absolutely worth every penny",
        "From start to finish, everything was seamless. The booking process was easy, "
        "the meeting point was clearly marked, and the experience itself exceeded all "
        "my expectations. A must-do activity.",
    ),
    (
        "Great tour, highly recommend",
        "We had a wonderful time. Our guide was friendly and informative, sharing "
        "stories and facts that you just can't find in guidebooks. The pace was "
        "perfect and the group size was just right.",
    ),
    (
        "Exceeded expectations",
        "I was a bit skeptical at first, but this turned out to be one of the best "
        "experiences of our entire vacation. The attention to detail was impressive "
        "and the whole experience felt very authentic.",
    ),
    (
        "A wonderful way to spend the day",
        "Such a lovely experience. The weather cooperated beautifully and our guide "
        "made sure everyone was comfortable and engaged throughout. Perfect for "
        "couples, families, or solo travelers alike.",
    ),
    (
        "Memorable and well-organized",
        "Everything ran like clockwork. Picked up on time, excellent commentary, "
        "and genuine local insight that made the experience special. I felt like "
        "I was seeing the destination through a local's eyes.",
    ),
    (
        "Loved every minute",
        "This was hands down the best thing we did on our trip. The guide's "
        "enthusiasm was infectious, the locations were stunning, and the whole "
        "experience was incredibly well thought out.",
    ),
    (
        "Perfect for first-time visitors",
        "If you're visiting for the first time, this is the activity to book. "
        "It gives you a fantastic overview and the guide provides excellent "
        "recommendations for the rest of your stay too.",
    ),
    (
        "Incredible value for money",
        "Honestly, I expected something decent but got something extraordinary. "
        "The quality of the experience far surpassed what I imagined at this price "
        "point. Don't think twice, just book it.",
    ),
    (
        "A truly authentic experience",
        "What sets this apart from other tourist activities is the genuine local "
        "flavor. We felt like insiders, not tourists. The personal touches and "
        "small details made all the difference.",
    ),
    (
        "Best activity of our trip",
        "We did a lot of activities during our vacation, and this one stood out "
        "above the rest. Well-paced, beautifully guided, and packed with moments "
        "that we'll remember for years to come.",
    ),
    (
        "Good experience with minor hiccups",
        "Overall a very enjoyable experience. The main activity was fantastic and "
        "our guide was excellent. There was a slight delay at the start, but it "
        "didn't really impact the overall quality.",
    ),
    (
        "Fun and educational",
        "I learned so much while having an absolute blast. The guide struck a "
        "perfect balance between being informative and entertaining. Great for "
        "curious travelers who want depth, not just surface-level tours.",
    ),
    (
        "Stunning scenery and great company",
        "The views alone would have been worth the price, but the guide's "
        "commentary and the group's energy made it so much better. Came back "
        "with hundreds of photos and amazing memories.",
    ),
    (
        "Would do it again in a heartbeat",
        "This is one of those experiences that I'd happily repeat on a return "
        "visit. Everything from the logistics to the actual experience was "
        "polished and professional. Top marks all around.",
    ),
    (
        "Solid experience, recommended",
        "We thoroughly enjoyed this activity. The guide was punctual, friendly, "
        "and clearly passionate about the subject. A few small things could be "
        "improved, but overall a great time.",
    ),
    (
        "A hidden gem of an activity",
        "I almost didn't book this, but I'm so glad I did. It turned out to be "
        "one of the most unique and rewarding things we did. The local perspective "
        "added so much richness to the experience.",
    ),
    (
        "Fantastic for the whole family",
        "We brought our kids along and everyone had a great time. The guide was "
        "patient and engaging with travelers of all ages. It's rare to find an "
        "activity that works equally well for adults and children.",
    ),
    (
        "Well worth the early start",
        "Yes, the early meeting time was tough on vacation, but the payoff was "
        "enormous. Fewer crowds, beautiful light, and an experience that felt "
        "exclusive. Our guide's energy was contagious.",
    ),
    (
        "Beautifully curated experience",
        "You can tell a lot of thought went into designing this activity. Every "
        "stop, every story, every detail felt intentional. It wasn't just a tour, "
        "it was a journey. Truly special.",
    ),
]


def run():
    session = Session()

    try:
        # Fix sequences
        print("Fixing sequences...")
        seq_fixes = [
            ("reviews", "id"),
            ("review_categories", "id"),
        ]
        for table, col in seq_fixes:
            session.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table}', '{col}'), "
                f"COALESCE((SELECT MAX({col}) FROM {table}), 0) + 1, false)"
            ))
        session.commit()
        print("  Sequences fixed.")

        # Get customer user IDs
        rows = session.execute(text(
            "SELECT id FROM users WHERE role = 'CUSTOMER' ORDER BY id"
        )).fetchall()
        customer_ids = [r[0] for r in rows]
        print(f"  Found {len(customer_ids)} customer users.")

        # Get activities with no reviews
        rows = session.execute(text(
            "SELECT a.id, a.vendor_id, a.title FROM activities a "
            "WHERE a.id NOT IN (SELECT DISTINCT activity_id FROM reviews) "
            "ORDER BY a.id"
        )).fetchall()
        activities_no_reviews = [(r[0], r[1], r[2]) for r in rows]
        print(f"  Found {len(activities_no_reviews)} activities with no reviews.\n")

        if not activities_no_reviews:
            print("All activities already have reviews. Nothing to do.")
            return

        review_count = 0
        base_date = datetime(2025, 3, 1, tzinfo=timezone.utc)

        for activity_id, vendor_id, title in activities_no_reviews:
            num_reviews = random.randint(3, 5)
            used_users = set()
            used_templates = set()
            templates = random.sample(range(len(REVIEW_TEMPLATES)), num_reviews)

            for i in range(num_reviews):
                # Pick a unique user for this activity
                user_id = random.choice(
                    [uid for uid in customer_ids if uid not in used_users]
                )
                used_users.add(user_id)

                # Rating weighted toward 4-5
                rating = random.choices([3, 4, 5], weights=[1, 3, 6])[0]

                template_idx = templates[i]
                review_title, comment = REVIEW_TEMPLATES[template_idx]

                helpful = random.randint(0, 15)
                created_at = base_date + timedelta(
                    days=random.randint(0, 365),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )

                session.execute(text(
                    "INSERT INTO reviews "
                    "(user_id, activity_id, vendor_id, rating, title, comment, "
                    "is_verified_booking, helpful_count, created_at) "
                    "VALUES (:user_id, :activity_id, :vendor_id, :rating, :title, "
                    ":comment, :is_verified, :helpful, :created_at)"
                ), {
                    "user_id": user_id,
                    "activity_id": activity_id,
                    "vendor_id": vendor_id,
                    "rating": rating,
                    "title": review_title,
                    "comment": comment,
                    "is_verified": True,
                    "helpful": helpful,
                    "created_at": created_at,
                })
                review_count += 1

            print(f"  + {num_reviews} reviews for: {title}")

        session.commit()
        print(f"\nInserted {review_count} reviews.")

        # Update average_rating and total_reviews for ALL activities
        print("\nUpdating activity statistics...")
        session.execute(text(
            "UPDATE activities a SET "
            "  total_reviews = sub.cnt, "
            "  average_rating = sub.avg_rating "
            "FROM ("
            "  SELECT activity_id, COUNT(*) AS cnt, "
            "  ROUND(AVG(rating)::numeric, 2) AS avg_rating "
            "  FROM reviews GROUP BY activity_id"
            ") sub "
            "WHERE a.id = sub.activity_id"
        ))
        session.commit()
        print("  Activity statistics updated.")

        # Verify
        row = session.execute(text(
            "SELECT COUNT(*) FROM reviews"
        )).fetchone()
        print(f"\n  Total reviews in database: {row[0]}")

        row = session.execute(text(
            "SELECT COUNT(*) FROM activities "
            "WHERE id NOT IN (SELECT DISTINCT activity_id FROM reviews)"
        )).fetchone()
        print(f"  Activities still without reviews: {row[0]}")

        print("\nDone!")

    except Exception as e:
        session.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
