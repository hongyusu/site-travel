"""Wishlist API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import User
from app.models.wishlist import Wishlist
from app.models.activity import Activity
from app.api.v1.auth import get_current_user

router = APIRouter()


@router.get("/wishlist")
def get_wishlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's wishlist."""
    wishlist_items = (
        db.query(Wishlist)
        .filter(Wishlist.user_id == current_user.id)
        .options(joinedload(Wishlist.activity))
        .all()
    )

    activities = []
    for item in wishlist_items:
        activity = item.activity
        if activity:
            # Get primary image
            primary_image = next((img for img in activity.images if img.is_primary), None)
            image_url = primary_image.url if primary_image else (activity.images[0].url if activity.images else None)

            # Get destinations
            destinations = [{"id": ad.destination.id, "name": ad.destination.name, "slug": ad.destination.slug}
                          for ad in activity.destinations]

            activities.append({
                "id": activity.id,
                "title": activity.title,
                "slug": activity.slug,
                "short_description": activity.short_description,
                "price_adult": float(activity.price_adult),
                "price_currency": activity.price_currency,
                "duration_minutes": activity.duration_minutes,
                "average_rating": float(activity.average_rating) if activity.average_rating else 0,
                "total_reviews": activity.total_reviews,
                "is_bestseller": activity.is_bestseller,
                "free_cancellation_hours": activity.free_cancellation_hours,
                "image_url": image_url,
                "destinations": destinations,
                "added_at": item.created_at.isoformat() if item.created_at else None
            })

    return {"success": True, "data": activities}


@router.post("/wishlist/{activity_id}")
def add_to_wishlist(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add activity to wishlist."""
    # Check if activity exists
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if already in wishlist
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.activity_id == activity_id
    ).first()

    if existing:
        return {
            "success": True,
            "message": "Activity already in wishlist",
            "data": {"activity_id": activity_id, "in_wishlist": True}
        }

    # Add to wishlist
    wishlist_item = Wishlist(user_id=current_user.id, activity_id=activity_id)
    db.add(wishlist_item)
    db.commit()

    return {
        "success": True,
        "message": "Activity added to wishlist",
        "data": {"activity_id": activity_id, "in_wishlist": True}
    }


@router.delete("/wishlist/{activity_id}")
def remove_from_wishlist(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove activity from wishlist."""
    wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.activity_id == activity_id
    ).first()

    if not wishlist_item:
        raise HTTPException(status_code=404, detail="Activity not in wishlist")

    db.delete(wishlist_item)
    db.commit()

    return {
        "success": True,
        "message": "Activity removed from wishlist",
        "data": {"activity_id": activity_id, "in_wishlist": False}
    }


@router.get("/wishlist/check/{activity_id}")
def check_in_wishlist(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if activity is in user's wishlist."""
    exists = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.activity_id == activity_id
    ).first() is not None

    return {
        "success": True,
        "data": {"activity_id": activity_id, "in_wishlist": exists}
    }
