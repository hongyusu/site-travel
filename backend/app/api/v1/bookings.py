"""Booking endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, date, timedelta
from decimal import Decimal

from app.database import get_db
from app.models import (
    Booking, Activity, User, Vendor, Availability,
    BookingStatus, ActivityImage
)
from app.schemas.booking import (
    BookingCreate, BookingUpdate, BookingResponse,
    AvailabilityCreate, AvailabilityResponse
)
from app.schemas.common import PaginatedResponse, MessageResponse
from app.api.deps import get_current_user, get_current_vendor, get_optional_current_user

router = APIRouter()


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Create a new booking.
    Can be done by authenticated users or guests.
    """
    # Get activity
    activity = db.query(Activity).filter(
        Activity.id == booking_data.activity_id,
        Activity.is_active == True
    ).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Check availability (simplified - in production, check actual availability)
    if booking_data.booking_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot book for past dates"
        )

    # Calculate total price
    total_participants = booking_data.adults + booking_data.children
    total_price = (
        activity.price_adult * booking_data.adults +
        (activity.price_child or 0) * booking_data.children
    )

    # Determine initial status based on activity settings
    if activity.instant_confirmation:
        initial_status = BookingStatus.CONFIRMED
    else:
        initial_status = BookingStatus.PENDING_VENDOR_APPROVAL

    # Create booking
    db_booking = Booking(
        user_id=current_user.id if current_user else None,
        activity_id=activity.id,
        vendor_id=activity.vendor_id,
        booking_date=booking_data.booking_date,
        booking_time=booking_data.booking_time,
        adults=booking_data.adults,
        children=booking_data.children,
        total_participants=total_participants,
        price_per_adult=activity.price_adult,
        price_per_child=activity.price_child,
        total_price=total_price,
        currency=activity.price_currency,
        status=initial_status,
        customer_name=booking_data.customer_name or (current_user.full_name if current_user else None),
        customer_email=booking_data.customer_email or (current_user.email if current_user else None),
        customer_phone=booking_data.customer_phone or (current_user.phone if current_user else None),
        special_requirements=booking_data.special_requirements
    )

    # Set confirmation timestamp if instant confirmation
    if activity.instant_confirmation:
        db_booking.confirmed_at = datetime.utcnow()

    db.add(db_booking)

    # Update activity booking count
    activity.total_bookings += 1

    try:
        db.commit()
        db.refresh(db_booking)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create booking"
        )

    # Prepare response
    return _prepare_booking_response(db_booking, activity, db)


@router.get("/my", response_model=PaginatedResponse[BookingResponse])
def get_my_bookings(
    status: Optional[BookingStatus] = Query(None, description="Filter by status"),
    upcoming_only: bool = Query(False, description="Show only upcoming bookings"),
    past_only: bool = Query(False, description="Show only past bookings"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's bookings."""
    query = db.query(Booking).filter(Booking.user_id == current_user.id)

    # Filter by status
    if status:
        query = query.filter(Booking.status == status)

    # Filter by date
    today = date.today()
    if upcoming_only:
        query = query.filter(Booking.booking_date >= today)
    elif past_only:
        query = query.filter(Booking.booking_date < today)

    # Order by booking date
    query = query.order_by(Booking.booking_date.desc(), Booking.created_at.desc())

    # Get total count
    total = query.count()

    # Pagination
    offset = (page - 1) * per_page
    bookings = query.offset(offset).limit(per_page).all()

    # Prepare response
    response_bookings = []
    for booking in bookings:
        activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
        response_bookings.append(_prepare_booking_response(booking, activity, db))

    return PaginatedResponse.create(
        data=response_bookings,
        page=page,
        per_page=per_page,
        total=total,
        message="Bookings retrieved"
    )


@router.get("/{booking_ref}", response_model=BookingResponse)
def get_booking(
    booking_ref: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Get booking details by reference."""
    booking = db.query(Booking).filter(Booking.booking_ref == booking_ref).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Check permission (user can only see their own bookings unless admin)
    if current_user:
        if booking.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this booking"
            )

    activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
    return _prepare_booking_response(booking, activity, db)


@router.put("/{booking_ref}/cancel", response_model=BookingResponse)
def cancel_booking(
    booking_ref: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel a booking."""
    booking = db.query(Booking).filter(
        Booking.booking_ref == booking_ref,
        Booking.user_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )

    if booking.status == BookingStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel completed booking"
        )

    # Check cancellation policy
    activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
    booking_datetime = datetime.combine(booking.booking_date, booking.booking_time or datetime.min.time())
    hours_until_activity = (booking_datetime - datetime.utcnow()).total_seconds() / 3600

    if hours_until_activity < activity.free_cancellation_hours:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Free cancellation period has expired. Must cancel at least {activity.free_cancellation_hours} hours before activity"
        )

    # Cancel booking
    booking.status = BookingStatus.CANCELLED
    booking.cancelled_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)

    return _prepare_booking_response(booking, activity, db)


@router.get("/{activity_id}/availability", response_model=List[AvailabilityResponse])
def get_activity_availability(
    activity_id: int,
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db)
):
    """Get availability for an activity within date range."""
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

    # Get availability records
    availability = db.query(Availability).filter(
        Availability.activity_id == activity_id,
        Availability.date >= start_date,
        Availability.date <= end_date,
        Availability.is_available == True
    ).order_by(Availability.date, Availability.start_time).all()

    # If no specific availability, create default availability
    if not availability:
        availability = []
        current_date = start_date
        while current_date <= end_date:
            # Skip past dates
            if current_date >= date.today():
                avail = Availability(
                    activity_id=activity_id,
                    date=current_date,
                    spots_available=activity.max_group_size or 20,
                    spots_total=activity.max_group_size or 20,
                    price_adult=activity.price_adult,
                    price_child=activity.price_child,
                    is_available=True
                )
                availability.append(AvailabilityResponse(
                    id=0,
                    date=current_date,
                    start_time=None,
                    end_time=None,
                    spots_available=avail.spots_available,
                    spots_total=avail.spots_total,
                    price_adult=avail.price_adult,
                    price_child=avail.price_child,
                    is_available=True
                ))
            current_date += timedelta(days=1)

        return availability

    return availability


# Vendor endpoints
@router.get("/vendor/bookings", response_model=PaginatedResponse[BookingResponse])
def get_vendor_bookings(
    status: Optional[BookingStatus] = Query(None, description="Filter by status"),
    booking_date: Optional[date] = Query(None, description="Filter by booking date"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_vendor: User = Depends(get_current_vendor)
):
    """Get bookings for vendor's activities."""
    query = db.query(Booking).filter(
        Booking.vendor_id == current_vendor.vendor_profile.id
    )

    # Filters
    if status:
        query = query.filter(Booking.status == status)

    if booking_date:
        query = query.filter(Booking.booking_date == booking_date)

    # Order by booking date
    query = query.order_by(Booking.booking_date.desc(), Booking.created_at.desc())

    # Get total count
    total = query.count()

    # Pagination
    offset = (page - 1) * per_page
    bookings = query.offset(offset).limit(per_page).all()

    # Prepare response
    response_bookings = []
    for booking in bookings:
        activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
        response_bookings.append(_prepare_booking_response(booking, activity, db))

    return PaginatedResponse.create(
        data=response_bookings,
        page=page,
        per_page=per_page,
        total=total,
        message="Vendor bookings retrieved"
    )


@router.patch("/vendor/{booking_id}/approve", response_model=BookingResponse)
def approve_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_vendor: User = Depends(get_current_vendor)
):
    """Approve a pending booking."""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.vendor_id == current_vendor.vendor_profile.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.status != BookingStatus.PENDING_VENDOR_APPROVAL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only approve bookings pending vendor approval"
        )

    # Approve booking
    booking.status = BookingStatus.CONFIRMED
    booking.confirmed_at = datetime.utcnow()
    booking.vendor_approved_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)

    activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
    return _prepare_booking_response(booking, activity, db)


@router.patch("/vendor/{booking_id}/reject", response_model=BookingResponse)
def reject_booking(
    booking_id: int,
    rejection_reason: str,
    db: Session = Depends(get_db),
    current_vendor: User = Depends(get_current_vendor)
):
    """Reject a pending booking."""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.vendor_id == current_vendor.vendor_profile.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.status != BookingStatus.PENDING_VENDOR_APPROVAL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only reject bookings pending vendor approval"
        )

    if not rejection_reason or len(rejection_reason.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejection reason is required"
        )

    # Reject booking
    booking.status = BookingStatus.REJECTED
    booking.rejection_reason = rejection_reason
    booking.vendor_rejected_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)

    activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
    return _prepare_booking_response(booking, activity, db)


@router.put("/vendor/{booking_id}/checkin", response_model=BookingResponse)
def checkin_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_vendor: User = Depends(get_current_vendor)
):
    """Mark a booking as checked in (completed)."""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.vendor_id == current_vendor.vendor_profile.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.status != BookingStatus.CONFIRMED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only check in confirmed bookings"
        )

    # Mark as completed
    booking.status = BookingStatus.COMPLETED
    booking.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)

    activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
    return _prepare_booking_response(booking, activity, db)


@router.post("/vendor/{booking_id}/cancel", response_model=BookingResponse)
def vendor_cancel_booking(
    booking_id: int,
    reason: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_vendor: User = Depends(get_current_vendor)
):
    """Vendor cancels a confirmed booking."""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.vendor_id == current_vendor.vendor_profile.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )

    if booking.status == BookingStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel completed booking"
        )

    if not reason or len(reason.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cancellation reason is required"
        )

    # Cancel booking
    booking.status = BookingStatus.CANCELLED
    booking.rejection_reason = reason  # Reuse this field for cancellation reason
    booking.cancelled_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)

    activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
    return _prepare_booking_response(booking, activity, db)


def _prepare_booking_response(booking: Booking, activity: Activity, db: Session) -> BookingResponse:
    """Helper function to prepare booking response."""
    # Get activity primary image
    primary_image = db.query(ActivityImage).filter(
        ActivityImage.activity_id == activity.id,
        ActivityImage.is_primary == True
    ).first()

    activity_info = {
        "id": activity.id,
        "title": activity.title,
        "slug": activity.slug,
        "primary_image": primary_image.url if primary_image else None,
        "duration_minutes": activity.duration_minutes
    }

    return BookingResponse(
        id=booking.id,
        booking_ref=booking.booking_ref,
        activity=activity_info,
        booking_date=booking.booking_date,
        booking_time=booking.booking_time,
        adults=booking.adults,
        children=booking.children,
        total_participants=booking.total_participants,
        total_price=booking.total_price,
        currency=booking.currency,
        status=booking.status,
        customer_name=booking.customer_name,
        customer_email=booking.customer_email,
        customer_phone=booking.customer_phone,
        special_requirements=booking.special_requirements,
        created_at=booking.created_at,
        confirmed_at=booking.confirmed_at
    )