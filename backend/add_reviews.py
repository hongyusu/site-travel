"""Add demo reviews to the database."""

import random
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Review, User, Activity, Vendor

# Sample review data
REVIEW_TEMPLATES = [
    {
        "rating": 5,
        "title": "Absolutely amazing experience!",
        "comment": "This was hands down one of the best tours we've ever been on. Our guide was incredibly knowledgeable and passionate about the history and culture. The pace was perfect, allowing us to really take in each location. Would highly recommend to anyone visiting!"
    },
    {
        "rating": 5,
        "title": "Exceeded expectations",
        "comment": "I can't say enough good things about this experience. Everything was well-organized, the guide was friendly and informative, and we got to see so much more than we expected. Worth every penny!"
    },
    {
        "rating": 5,
        "title": "Must-do activity!",
        "comment": "If you're planning your trip, make sure to book this! It was the highlight of our vacation. The guide made the experience so enjoyable and we learned so much. Can't wait to come back and do it again."
    },
    {
        "rating": 5,
        "title": "Perfect for families",
        "comment": "We brought our kids (ages 8 and 12) and they loved it! The guide was great with children and kept everyone engaged. Highly recommend for families looking for an educational and fun experience."
    },
    {
        "rating": 4,
        "title": "Great experience overall",
        "comment": "Really enjoyed this tour. The guide was knowledgeable and friendly. Only giving 4 stars because it was quite crowded, but that's to be expected during peak season. Still highly recommend!"
    },
    {
        "rating": 4,
        "title": "Very good tour",
        "comment": "Had a great time on this tour. The guide was excellent and we saw all the main sights. Would have liked a bit more time at some locations, but overall a very good experience."
    },
    {
        "rating": 4,
        "title": "Well organized and informative",
        "comment": "The tour was well-organized and our guide clearly knew their stuff. We learned a lot and had a good time. The only minor issue was that the group was a bit large, making it hard to hear at times."
    },
    {
        "rating": 4,
        "title": "Worth the money",
        "comment": "Good value for the price. The guide was professional and the itinerary was well-planned. We got to see and learn about many interesting places. Would recommend!"
    },
    {
        "rating": 3,
        "title": "Decent but could be better",
        "comment": "The tour was okay, but didn't quite live up to the hype. Our guide was nice enough but seemed rushed. We didn't get as much time as I'd hoped at each location. It's not bad, just average."
    },
    {
        "rating": 3,
        "title": "Average experience",
        "comment": "It was fine, nothing special. The guide did their job and we saw the sights, but I didn't feel like I learned anything new or had a memorable experience. Probably wouldn't do it again."
    },
    {
        "rating": 2,
        "title": "Disappointing",
        "comment": "Unfortunately, this didn't meet our expectations. The guide seemed inexperienced and we felt rushed through everything. For the price, I expected much better."
    },
    {
        "rating": 1,
        "title": "Not recommended",
        "comment": "Very disappointed with this experience. The guide showed up late, was disorganized, and didn't seem to know much about the area. We left early and requested a refund."
    }
]


def add_reviews():
    """Add demo reviews to activities."""
    db = SessionLocal()

    try:
        # Get customer user
        customer = db.query(User).filter(User.email == "customer@example.com").first()
        if not customer:
            print("Error: Customer user not found")
            return

        # Get all activities
        activities = db.query(Activity).all()

        if not activities:
            print("Error: No activities found")
            return

        print(f"Adding reviews for {len(activities)} activities...")
        total_reviews = 0

        for activity in activities:
            # Get vendor for this activity
            vendor = db.query(Vendor).filter(Vendor.id == activity.vendor_id).first()
            if not vendor:
                print(f"Warning: No vendor found for activity {activity.id}")
                continue

            # Add 5-10 reviews per activity
            num_reviews = random.randint(5, 10)

            for i in range(num_reviews):
                # Select review template based on weighted distribution
                # 60% 5-star, 25% 4-star, 10% 3-star, 5% 1-2 star
                rand = random.random()
                if rand < 0.60:
                    rating_range = [r for r in REVIEW_TEMPLATES if r["rating"] == 5]
                elif rand < 0.85:
                    rating_range = [r for r in REVIEW_TEMPLATES if r["rating"] == 4]
                elif rand < 0.95:
                    rating_range = [r for r in REVIEW_TEMPLATES if r["rating"] == 3]
                else:
                    rating_range = [r for r in REVIEW_TEMPLATES if r["rating"] in [1, 2]]

                template = random.choice(rating_range)

                # Create review with date in the past 6 months
                days_ago = random.randint(1, 180)
                created_at = datetime.now() - timedelta(days=days_ago)

                review = Review(
                    user_id=customer.id,
                    activity_id=activity.id,
                    vendor_id=vendor.id,
                    rating=template["rating"],
                    title=template["title"],
                    comment=template["comment"],
                    is_verified_booking=True,
                    helpful_count=random.randint(0, 25),
                    created_at=created_at
                )
                db.add(review)
                total_reviews += 1

            # Update activity average rating and review count
            activity_reviews = db.query(Review).filter(Review.activity_id == activity.id).all()
            if activity_reviews:
                avg_rating = sum(r.rating for r in activity_reviews) / len(activity_reviews)
                activity.average_rating = round(avg_rating, 1)
                activity.total_reviews = len(activity_reviews)

        db.commit()
        print(f"Successfully added {total_reviews} reviews!")
        print("\nReview distribution by activity:")

        for activity in activities:
            review_count = db.query(Review).filter(Review.activity_id == activity.id).count()
            print(f"  {activity.title}: {review_count} reviews (avg rating: {activity.average_rating})")

    except Exception as e:
        print(f"Error adding reviews: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_reviews()
