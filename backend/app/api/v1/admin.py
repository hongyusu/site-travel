"""Admin endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, Vendor, Activity, Booking, Review, UserRole, ActivityCategory, Category
from app.schemas.common import PaginatedResponse, MessageResponse
from app.api.deps import get_current_admin

router = APIRouter()


@router.get("/stats")
def get_platform_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Get platform statistics."""
    # User stats
    total_users = db.query(User).count()
    total_customers = db.query(User).filter(User.role == UserRole.CUSTOMER).count()
    total_vendors = db.query(User).filter(User.role == UserRole.VENDOR).count()

    # Activity stats
    total_activities = db.query(Activity).count()
    active_activities = db.query(Activity).filter(Activity.is_active == True).count()

    # Booking stats
    total_bookings = db.query(Booking).count()
    total_revenue = db.query(func.sum(Booking.total_price)).scalar() or 0

    # Recent bookings (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_bookings = db.query(Booking).filter(
        Booking.created_at >= thirty_days_ago
    ).count()
    recent_revenue = db.query(func.sum(Booking.total_price)).filter(
        Booking.created_at >= thirty_days_ago
    ).scalar() or 0

    # Review stats
    total_reviews = db.query(Review).count()
    avg_rating = db.query(func.avg(Review.rating)).scalar() or 0

    # Top activities by bookings
    top_activities = db.query(
        Activity.id,
        Activity.title,
        func.count(Booking.id).label('booking_count')
    ).join(Booking).group_by(Activity.id, Activity.title).order_by(
        desc('booking_count')
    ).limit(5).all()

    return {
        "success": True,
        "data": {
            "users": {
                "total": total_users,
                "customers": total_customers,
                "vendors": total_vendors
            },
            "activities": {
                "total": total_activities,
                "active": active_activities,
                "inactive": total_activities - active_activities
            },
            "bookings": {
                "total": total_bookings,
                "last_30_days": recent_bookings
            },
            "revenue": {
                "total": float(total_revenue),
                "last_30_days": float(recent_revenue)
            },
            "reviews": {
                "total": total_reviews,
                "average_rating": round(float(avg_rating), 2)
            },
            "top_activities": [
                {
                    "id": a.id,
                    "title": a.title,
                    "booking_count": a.booking_count
                }
                for a in top_activities
            ]
        }
    }


@router.get("/users")
def list_users(
    role: Optional[str] = Query(None, description="Filter by role"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """List all users."""
    query = db.query(User)

    if role:
        try:
            user_role = UserRole[role.upper()]
            query = query.filter(User.role == user_role)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role: {role}"
            )

    query = query.order_by(desc(User.created_at))

    total = query.count()
    offset = (page - 1) * per_page
    users = query.offset(offset).limit(per_page).all()

    return PaginatedResponse.create(
        data=[
            {
                "id": u.id,
                "email": u.email,
                "full_name": u.full_name,
                "role": u.role.value,
                "is_active": u.is_active,
                "created_at": u.created_at
            }
            for u in users
        ],
        page=page,
        per_page=per_page,
        total=total,
        message="Users retrieved"
    )


@router.patch("/users/{user_id}/toggle-status")
def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Toggle user active status."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify admin users"
        )

    user.is_active = not user.is_active
    db.commit()

    return {
        "success": True,
        "data": {
            "id": user.id,
            "is_active": user.is_active
        },
        "message": f"User {'activated' if user.is_active else 'deactivated'}"
    }


@router.get("/vendors")
def list_vendors(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """List all vendors with their activities."""
    query = db.query(Vendor).join(User).order_by(desc(Vendor.created_at))

    total = query.count()
    offset = (page - 1) * per_page
    vendors = query.offset(offset).limit(per_page).all()

    result = []
    for vendor in vendors:
        user = db.query(User).filter(User.id == vendor.user_id).first()
        activity_count = db.query(Activity).filter(Activity.vendor_id == vendor.id).count()
        active_activity_count = db.query(Activity).filter(
            Activity.vendor_id == vendor.id,
            Activity.is_active == True
        ).count()
        total_bookings = db.query(Booking).join(Activity).filter(
            Activity.vendor_id == vendor.id
        ).count()

        result.append({
            "id": vendor.id,
            "user_id": vendor.user_id,
            "email": user.email if user else None,
            "company_name": vendor.company_name,
            "is_verified": vendor.is_verified,
            "activity_count": activity_count,
            "active_activity_count": active_activity_count,
            "total_bookings": total_bookings,
            "created_at": vendor.created_at
        })

    return PaginatedResponse.create(
        data=result,
        page=page,
        per_page=per_page,
        total=total,
        message="Vendors retrieved"
    )


@router.patch("/vendors/{vendor_id}/verify")
def toggle_vendor_verification(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Toggle vendor verification status."""
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )

    vendor.is_verified = not vendor.is_verified
    db.commit()

    return {
        "success": True,
        "data": {
            "id": vendor.id,
            "is_verified": vendor.is_verified
        },
        "message": f"Vendor {'verified' if vendor.is_verified else 'unverified'}"
    }


@router.get("/activities")
def list_all_activities(
    status_filter: Optional[str] = Query(None, description="Filter by status: active, inactive"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """List all activities for moderation."""
    query = db.query(Activity)

    if status_filter == "active":
        query = query.filter(Activity.is_active == True)
    elif status_filter == "inactive":
        query = query.filter(Activity.is_active == False)

    query = query.order_by(desc(Activity.created_at))

    total = query.count()
    offset = (page - 1) * per_page
    activities = query.offset(offset).limit(per_page).all()

    result = []
    for activity in activities:
        vendor = db.query(Vendor).filter(Vendor.id == activity.vendor_id).first()
        booking_count = db.query(Booking).filter(Booking.activity_id == activity.id).count()

        # Get categories for this activity
        categories = db.query(Category).join(ActivityCategory).filter(
            ActivityCategory.activity_id == activity.id
        ).all()
        category_names = [cat.name for cat in categories] if categories else []

        result.append({
            "id": activity.id,
            "title": activity.title,
            "slug": activity.slug,
            "vendor_name": vendor.company_name if vendor else None,
            "categories": category_names,
            "price_adult": float(activity.price_adult),
            "is_active": activity.is_active,
            "average_rating": float(activity.average_rating) if activity.average_rating else None,
            "total_reviews": activity.total_reviews,
            "total_bookings": booking_count,
            "created_at": activity.created_at
        })

    return PaginatedResponse.create(
        data=result,
        page=page,
        per_page=per_page,
        total=total,
        message="Activities retrieved"
    )


@router.patch("/activities/{activity_id}/toggle-status")
def admin_toggle_activity_status(
    activity_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Admin toggle activity status."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    activity.is_active = not activity.is_active
    db.commit()

    return {
        "success": True,
        "data": {
            "id": activity.id,
            "is_active": activity.is_active
        },
        "message": f"Activity {'activated' if activity.is_active else 'deactivated'}"
    }


@router.delete("/activities/{activity_id}")
def admin_delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Admin delete activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Check if there are any bookings
    booking_count = db.query(Booking).filter(Booking.activity_id == activity_id).count()
    if booking_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete activity with {booking_count} existing bookings"
        )

    db.delete(activity)
    db.commit()

    return MessageResponse(message="Activity deleted successfully")


@router.get("/bookings")
def list_all_bookings(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """List all bookings."""
    query = db.query(Booking).order_by(desc(Booking.created_at))

    total = query.count()
    offset = (page - 1) * per_page
    bookings = query.offset(offset).limit(per_page).all()

    result = []
    for booking in bookings:
        user = db.query(User).filter(User.id == booking.user_id).first()
        activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()

        result.append({
            "id": booking.id,
            "booking_reference": booking.booking_reference,
            "customer_name": user.full_name if user else None,
            "customer_email": user.email if user else None,
            "activity_title": activity.title if activity else None,
            "booking_date": booking.booking_date,
            "adults": booking.adults,
            "children": booking.children,
            "total_price": float(booking.total_price),
            "status": booking.status.value,
            "created_at": booking.created_at
        })

    return PaginatedResponse.create(
        data=result,
        page=page,
        per_page=per_page,
        total=total,
        message="Bookings retrieved"
    )


@router.get("/reviews")
def list_all_reviews(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """List all reviews for moderation."""
    query = db.query(Review).order_by(desc(Review.created_at))

    total = query.count()
    offset = (page - 1) * per_page
    reviews = query.offset(offset).limit(per_page).all()

    result = []
    for review in reviews:
        user = db.query(User).filter(User.id == review.user_id).first()
        activity = db.query(Activity).filter(Activity.id == review.activity_id).first()

        result.append({
            "id": review.id,
            "user_name": user.full_name if user else None,
            "activity_title": activity.title if activity else None,
            "rating": review.rating,
            "title": review.title,
            "comment": review.comment,
            "is_verified_booking": review.is_verified_booking,
            "helpful_count": review.helpful_count,
            "created_at": review.created_at
        })

    return PaginatedResponse.create(
        data=result,
        page=page,
        per_page=per_page,
        total=total,
        message="Reviews retrieved"
    )


@router.delete("/reviews/{review_id}")
def admin_delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Admin delete review."""
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # Update activity stats
    activity = db.query(Activity).filter(Activity.id == review.activity_id).first()
    if activity:
        remaining_reviews = db.query(Review).filter(
            Review.activity_id == activity.id,
            Review.id != review_id
        ).all()

        if remaining_reviews:
            avg_rating = sum(r.rating for r in remaining_reviews) / len(remaining_reviews)
            activity.average_rating = round(avg_rating, 1)
            activity.total_reviews = len(remaining_reviews)
        else:
            activity.average_rating = 0
            activity.total_reviews = 0

    db.delete(review)
    db.commit()

    return MessageResponse(message="Review deleted successfully")
