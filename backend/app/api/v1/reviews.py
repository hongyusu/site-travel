"""Review endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.database import get_db
from app.models import Review, ReviewImage, Activity, Booking, User, BookingStatus
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/activity/{activity_id}", response_model=PaginatedResponse[ReviewResponse])
def get_activity_reviews(
    activity_id: int,
    rating: Optional[int] = Query(None, ge=1, le=5, description="Filter by rating"),
    verified_only: bool = Query(False, description="Only verified bookings"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get reviews for an activity."""
    # Validate activity
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.is_active == True
    ).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Build query
    query = db.query(Review).filter(Review.activity_id == activity_id)

    # Filters
    if rating:
        query = query.filter(Review.rating == rating)

    if verified_only:
        query = query.filter(Review.is_verified_booking == True)

    # Order by most helpful and recent
    query = query.order_by(Review.helpful_count.desc(), Review.created_at.desc())

    # Get total count
    total = query.count()

    # Pagination
    offset = (page - 1) * per_page
    reviews = query.offset(offset).limit(per_page).all()

    # Prepare response
    response_reviews = []
    for review in reviews:
        user = db.query(User).filter(User.id == review.user_id).first()
        images = db.query(ReviewImage).filter(ReviewImage.review_id == review.id).all()

        response_reviews.append(ReviewResponse(
            id=review.id,
            user={
                "id": user.id,
                "name": user.full_name,
                "avatar": None  # Could add avatar URL if we had it
            },
            rating=review.rating,
            title=review.title,
            comment=review.comment,
            is_verified_booking=review.is_verified_booking,
            helpful_count=review.helpful_count,
            created_at=review.created_at,
            images=images
        ))

    return PaginatedResponse.create(
        data=response_reviews,
        page=page,
        per_page=per_page,
        total=total,
        message="Reviews retrieved"
    )


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new review."""
    # Validate activity
    activity = db.query(Activity).filter(
        Activity.id == review_data.activity_id,
        Activity.is_active == True
    ).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Check if user has already reviewed this activity
    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.activity_id == review_data.activity_id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this activity"
        )

    # Check if review is for a verified booking
    is_verified = False
    booking = None

    if review_data.booking_id:
        booking = db.query(Booking).filter(
            Booking.id == review_data.booking_id,
            Booking.user_id == current_user.id,
            Booking.activity_id == review_data.activity_id,
            Booking.status == BookingStatus.COMPLETED
        ).first()

        if booking:
            is_verified = True

    # Create review
    db_review = Review(
        user_id=current_user.id,
        activity_id=review_data.activity_id,
        vendor_id=activity.vendor_id,
        booking_id=review_data.booking_id if booking else None,
        rating=review_data.rating,
        title=review_data.title,
        comment=review_data.comment,
        is_verified_booking=is_verified
    )

    db.add(db_review)

    # Update activity rating
    _update_activity_rating(activity, db)

    try:
        db.commit()
        db.refresh(db_review)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create review"
        )

    # Prepare response
    return ReviewResponse(
        id=db_review.id,
        user={
            "id": current_user.id,
            "name": current_user.full_name,
            "avatar": None
        },
        rating=db_review.rating,
        title=db_review.title,
        comment=db_review.comment,
        is_verified_booking=db_review.is_verified_booking,
        helpful_count=db_review.helpful_count,
        created_at=db_review.created_at,
        images=[]
    )


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a review."""
    review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == current_user.id
    ).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # Update fields
    if review_update.rating is not None:
        review.rating = review_update.rating
    if review_update.title is not None:
        review.title = review_update.title
    if review_update.comment is not None:
        review.comment = review_update.comment

    review.updated_at = datetime.utcnow()

    # Update activity rating
    activity = db.query(Activity).filter(Activity.id == review.activity_id).first()
    _update_activity_rating(activity, db)

    db.commit()
    db.refresh(review)

    # Prepare response
    images = db.query(ReviewImage).filter(ReviewImage.review_id == review.id).all()

    return ReviewResponse(
        id=review.id,
        user={
            "id": current_user.id,
            "name": current_user.full_name,
            "avatar": None
        },
        rating=review.rating,
        title=review.title,
        comment=review.comment,
        is_verified_booking=review.is_verified_booking,
        helpful_count=review.helpful_count,
        created_at=review.created_at,
        images=images
    )


@router.delete("/{review_id}", response_model=MessageResponse)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a review."""
    review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == current_user.id
    ).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    activity_id = review.activity_id

    db.delete(review)

    # Update activity rating
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    _update_activity_rating(activity, db)

    db.commit()

    return MessageResponse(message="Review deleted successfully")


@router.post("/{review_id}/helpful", response_model=MessageResponse)
def mark_review_helpful(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a review as helpful."""
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    if review.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot mark your own review as helpful"
        )

    # Increment helpful count
    review.helpful_count += 1
    db.commit()

    return MessageResponse(message="Review marked as helpful")


@router.get("/my", response_model=PaginatedResponse[ReviewResponse])
def get_my_reviews(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's reviews."""
    query = db.query(Review).filter(Review.user_id == current_user.id)
    query = query.order_by(Review.created_at.desc())

    # Get total count
    total = query.count()

    # Pagination
    offset = (page - 1) * per_page
    reviews = query.offset(offset).limit(per_page).all()

    # Prepare response
    response_reviews = []
    for review in reviews:
        activity = db.query(Activity).filter(Activity.id == review.activity_id).first()
        images = db.query(ReviewImage).filter(ReviewImage.review_id == review.id).all()

        response_reviews.append(ReviewResponse(
            id=review.id,
            user={
                "id": current_user.id,
                "name": current_user.full_name,
                "avatar": None
            },
            rating=review.rating,
            title=review.title,
            comment=review.comment,
            is_verified_booking=review.is_verified_booking,
            helpful_count=review.helpful_count,
            created_at=review.created_at,
            images=images
        ))

    return PaginatedResponse.create(
        data=response_reviews,
        page=page,
        per_page=per_page,
        total=total,
        message="Your reviews"
    )


def _update_activity_rating(activity: Activity, db: Session):
    """Helper function to update activity average rating."""
    # Calculate new average rating
    result = db.query(
        func.avg(Review.rating).label("avg_rating"),
        func.count(Review.id).label("total_reviews")
    ).filter(Review.activity_id == activity.id).first()

    if result.avg_rating:
        activity.average_rating = round(result.avg_rating, 1)
        activity.total_reviews = result.total_reviews
    else:
        activity.average_rating = 0
        activity.total_reviews = 0