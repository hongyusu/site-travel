"""Add images to some reviews."""

import random
from sqlalchemy import text
from app.database import SessionLocal
from app.models import Review, ReviewImage


def add_review_images():
    """Add images to 30-40% of reviews."""
    db = SessionLocal()

    try:
        # Get all reviews
        reviews = db.query(Review).all()
        print(f"Found {len(reviews)} reviews")

        # Select 30-40% of reviews to add images to
        num_reviews_with_images = int(len(reviews) * random.uniform(0.3, 0.4))
        reviews_to_update = random.sample(reviews, num_reviews_with_images)

        image_count = 0

        for review in reviews_to_update:
            # Add 1-3 images per review
            num_images = random.randint(1, 3)

            for i in range(num_images):
                # Use picsum.photos with seed for consistent images
                image_url = f"https://picsum.photos/seed/review-{review.id}-{i}/800/600"

                image = ReviewImage(
                    review_id=review.id,
                    url=image_url,
                    caption=f"Experience photo {i+1}"
                )
                db.add(image)
                image_count += 1

        db.commit()
        print(f"\n✅ Successfully added {image_count} review images!")
        print(f"   Reviews with images: {num_reviews_with_images} out of {len(reviews)} ({num_reviews_with_images/len(reviews)*100:.1f}%)")

        # Show sample
        print("\nSample review with images:")
        first_review_with_images = reviews_to_update[0]
        images = db.query(ReviewImage).filter(
            ReviewImage.review_id == first_review_with_images.id
        ).all()
        print(f"  Review ID: {first_review_with_images.id}")
        print(f"  Images: {len(images)}")
        for img in images:
            print(f"    - {img.url}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_review_images()
