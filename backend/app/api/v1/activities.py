"""Activity endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from decimal import Decimal

from app.database import get_db
from app.models import (
    Activity, Category, Destination, ActivityImage,
    ActivityCategory, ActivityDestination, ActivityHighlight,
    ActivityInclude, ActivityFAQ, MeetingPoint, Vendor,
    ActivityTimeline, ActivityTimeSlot, ActivityPricingTier,
    ActivityAddOn, MeetingPointPhoto
)
from app.schemas.activity import (
    ActivityResponse, ActivityDetailResponse, ActivitySearchParams,
    CategoryResponse, DestinationResponse, ActivityCreate, ActivityUpdate
)
from app.schemas.common import PaginationParams, PaginatedResponse
from app.api.deps import get_optional_current_user, get_current_vendor
from slugify import slugify

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):
    """Get all categories."""
    categories = db.query(Category).order_by(Category.order_index).all()
    return categories


@router.get("/destinations", response_model=List[DestinationResponse])
def get_destinations(
    featured_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all destinations."""
    query = db.query(Destination)

    if featured_only:
        query = query.filter(Destination.is_featured == True)

    destinations = query.order_by(Destination.name).all()
    return destinations


@router.get("/destinations/{slug}", response_model=DestinationResponse)
def get_destination_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get destination by slug."""
    destination = db.query(Destination).filter(Destination.slug == slug).first()

    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )

    return destination


@router.get("/search", response_model=PaginatedResponse[ActivityResponse])
def search_activities(
    q: Optional[str] = Query(None, description="Search query"),
    destination_id: Optional[int] = Query(None, description="Destination ID"),
    destination_slug: Optional[str] = Query(None, description="Destination slug"),
    category_id: Optional[int] = Query(None, description="Category ID"),
    category_slug: Optional[str] = Query(None, description="Category slug"),
    min_price: Optional[Decimal] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[Decimal] = Query(None, ge=0, description="Maximum price"),
    min_duration: Optional[int] = Query(None, ge=0, description="Min duration in minutes"),
    max_duration: Optional[int] = Query(None, ge=0, description="Max duration in minutes"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    languages: Optional[List[str]] = Query(None, description="Languages"),
    free_cancellation: Optional[bool] = Query(None, description="Free cancellation only"),
    instant_confirmation: Optional[bool] = Query(None, description="Instant confirmation only"),
    skip_the_line: Optional[bool] = Query(None, description="Skip the line only"),
    bestseller: Optional[bool] = Query(None, description="Bestsellers only"),
    vendor_only: Optional[bool] = Query(None, description="Show only current vendor's activities"),
    sort_by: str = Query("recommended", description="Sort: recommended, price_asc, price_desc, rating, duration"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user = Depends(get_optional_current_user)
):
    """
    Search and filter activities.
    """
    # Base query with eager loading
    # For vendor_only queries, show all activities (including inactive ones)
    # For public queries, only show active activities
    if vendor_only and current_user:
        query = db.query(Activity)
    else:
        query = db.query(Activity).filter(Activity.is_active == True)

    # Join for filtering
    if destination_id or destination_slug or category_id or category_slug:
        if destination_id or destination_slug:
            query = query.join(ActivityDestination).join(Destination)
            if destination_id:
                query = query.filter(Destination.id == destination_id)
            if destination_slug:
                query = query.filter(Destination.slug == destination_slug)

        if category_id or category_slug:
            query = query.join(ActivityCategory).join(Category)
            if category_id:
                query = query.filter(Category.id == category_id)
            if category_slug:
                query = query.filter(Category.slug == category_slug)

    # Text search
    if q:
        search_filter = or_(
            Activity.title.ilike(f"%{q}%"),
            Activity.description.ilike(f"%{q}%"),
            Activity.short_description.ilike(f"%{q}%")
        )
        query = query.filter(search_filter)

    # Price filter
    if min_price is not None:
        query = query.filter(Activity.price_adult >= min_price)
    if max_price is not None:
        query = query.filter(Activity.price_adult <= max_price)

    # Duration filter
    if min_duration is not None:
        query = query.filter(Activity.duration_minutes >= min_duration)
    if max_duration is not None:
        query = query.filter(Activity.duration_minutes <= max_duration)

    # Rating filter
    if min_rating is not None:
        query = query.filter(Activity.average_rating >= min_rating)

    # Languages filter
    if languages:
        for language in languages:
            query = query.filter(Activity.languages.contains([language]))

    # Boolean filters
    if free_cancellation is not None:
        if free_cancellation:
            query = query.filter(Activity.free_cancellation_hours > 0)
        else:
            query = query.filter(Activity.free_cancellation_hours == 0)

    if instant_confirmation is not None:
        query = query.filter(Activity.instant_confirmation == instant_confirmation)

    if skip_the_line is not None:
        query = query.filter(Activity.is_skip_the_line == skip_the_line)

    if bestseller is not None:
        query = query.filter(Activity.is_bestseller == bestseller)

    # Vendor filter
    if vendor_only and current_user:
        # Get vendor ID from current user
        vendor = db.query(Vendor).filter(Vendor.user_id == current_user.id).first()
        if vendor:
            query = query.filter(Activity.vendor_id == vendor.id)
        else:
            # If vendor_only is True but user is not a vendor, return empty results
            return PaginatedResponse.create(
                data=[],
                page=page,
                per_page=per_page,
                total=0,
                message="No activities found"
            )

    # Get total count
    total = query.count()

    # Sorting
    if sort_by == "price_asc":
        query = query.order_by(Activity.price_adult.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Activity.price_adult.desc())
    elif sort_by == "rating":
        query = query.order_by(Activity.average_rating.desc())
    elif sort_by == "duration":
        query = query.order_by(Activity.duration_minutes.asc())
    else:  # recommended
        query = query.order_by(
            Activity.is_bestseller.desc(),
            Activity.average_rating.desc(),
            Activity.total_bookings.desc()
        )

    # Pagination
    offset = (page - 1) * per_page
    activities = query.offset(offset).limit(per_page).all()

    # Prepare response with eager loading
    response_activities = []
    for activity in activities:
        # Get primary image
        primary_image = db.query(ActivityImage).filter(
            ActivityImage.activity_id == activity.id,
            ActivityImage.is_primary == True
        ).first()

        # Get categories
        activity_categories = db.query(Category).join(ActivityCategory).filter(
            ActivityCategory.activity_id == activity.id
        ).all()

        # Get destinations
        activity_destinations = db.query(Destination).join(ActivityDestination).filter(
            ActivityDestination.activity_id == activity.id
        ).all()

        activity_dict = {
            "id": activity.id,
            "title": activity.title,
            "slug": activity.slug,
            "short_description": activity.short_description,
            "price_adult": activity.price_adult,
            "price_child": activity.price_child,
            "duration_minutes": activity.duration_minutes,
            "average_rating": float(activity.average_rating) if activity.average_rating else 0,
            "total_reviews": activity.total_reviews,
            "is_bestseller": activity.is_bestseller,
            "is_skip_the_line": activity.is_skip_the_line,
            "is_active": activity.is_active,
            "free_cancellation_hours": activity.free_cancellation_hours,
            "languages": activity.languages,
            "primary_image": primary_image,
            "categories": activity_categories,
            "destinations": activity_destinations
        }
        response_activities.append(ActivityResponse(**activity_dict))

    return PaginatedResponse.create(
        data=response_activities,
        page=page,
        per_page=per_page,
        total=total,
        message="Activities found"
    )


@router.get("/slug/{slug}", response_model=ActivityDetailResponse)
def get_activity_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_optional_current_user)
):
    """Get activity details by slug."""
    activity = db.query(Activity).filter(
        Activity.slug == slug,
        Activity.is_active == True
    ).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    return _get_activity_details(activity, db)


def _get_activity_details(activity: Activity, db: Session) -> ActivityDetailResponse:
    """Helper function to get detailed activity information."""
    # Load related data
    images = db.query(ActivityImage).filter(
        ActivityImage.activity_id == activity.id
    ).order_by(ActivityImage.order_index).all()

    categories = db.query(Category).join(ActivityCategory).filter(
        ActivityCategory.activity_id == activity.id
    ).all()

    destinations = db.query(Destination).join(ActivityDestination).filter(
        ActivityDestination.activity_id == activity.id
    ).all()

    highlights = db.query(ActivityHighlight).filter(
        ActivityHighlight.activity_id == activity.id
    ).order_by(ActivityHighlight.order_index).all()

    includes = db.query(ActivityInclude).filter(
        ActivityInclude.activity_id == activity.id
    ).order_by(ActivityInclude.order_index).all()

    faqs = db.query(ActivityFAQ).filter(
        ActivityFAQ.activity_id == activity.id
    ).order_by(ActivityFAQ.order_index).all()

    meeting_point = db.query(MeetingPoint).filter(
        MeetingPoint.activity_id == activity.id
    ).first()

    # Load meeting point photos if meeting point exists
    if meeting_point:
        meeting_point.photos = db.query(MeetingPointPhoto).filter(
            MeetingPointPhoto.meeting_point_id == meeting_point.id
        ).order_by(MeetingPointPhoto.order_index).all()

    # Load new enhanced data
    timelines = db.query(ActivityTimeline).filter(
        ActivityTimeline.activity_id == activity.id
    ).order_by(ActivityTimeline.order_index).all()

    time_slots = db.query(ActivityTimeSlot).filter(
        ActivityTimeSlot.activity_id == activity.id
    ).order_by(ActivityTimeSlot.slot_time).all()

    pricing_tiers = db.query(ActivityPricingTier).filter(
        ActivityPricingTier.activity_id == activity.id,
        ActivityPricingTier.is_active == True
    ).order_by(ActivityPricingTier.order_index).all()

    add_ons = db.query(ActivityAddOn).filter(
        ActivityAddOn.activity_id == activity.id
    ).order_by(ActivityAddOn.order_index).all()

    # Get vendor info
    vendor = db.query(Vendor).filter(Vendor.id == activity.vendor_id).first()

    # Prepare response
    primary_image = next((img for img in images if img.is_primary), None)

    response_dict = {
        "id": activity.id,
        "title": activity.title,
        "slug": activity.slug,
        "short_description": activity.short_description,
        "description": activity.description,
        "price_adult": activity.price_adult,
        "price_child": activity.price_child,
        "duration_minutes": activity.duration_minutes,
        "max_group_size": activity.max_group_size,
        "instant_confirmation": activity.instant_confirmation,
        "free_cancellation_hours": activity.free_cancellation_hours,
        "languages": activity.languages,
        "average_rating": float(activity.average_rating) if activity.average_rating else 0,
        "total_reviews": activity.total_reviews,
        "total_bookings": activity.total_bookings,
        "is_bestseller": activity.is_bestseller,
        "is_skip_the_line": activity.is_skip_the_line,
        "is_active": activity.is_active,
        "primary_image": primary_image,
        "images": images,
        "categories": categories,
        "destinations": destinations,
        "highlights": highlights,
        "includes": includes,
        "faqs": faqs,
        "meeting_point": meeting_point,
        "vendor": {
            "id": vendor.id,
            "company_name": vendor.company_name,
            "is_verified": vendor.is_verified
        },
        # New enhanced fields
        "has_multiple_tiers": activity.has_multiple_tiers,
        "discount_percentage": activity.discount_percentage,
        "original_price_adult": activity.original_price_adult,
        "original_price_child": activity.original_price_child,
        "is_likely_to_sell_out": activity.is_likely_to_sell_out,
        "has_mobile_ticket": activity.has_mobile_ticket,
        "has_best_price_guarantee": activity.has_best_price_guarantee,
        "is_verified_activity": activity.is_verified_activity,
        "response_time_hours": activity.response_time_hours,
        "is_wheelchair_accessible": activity.is_wheelchair_accessible,
        "is_stroller_accessible": activity.is_stroller_accessible,
        "allows_service_animals": activity.allows_service_animals,
        "has_infant_seats": activity.has_infant_seats,
        "video_url": activity.video_url,
        "dress_code": activity.dress_code,
        "weather_dependent": activity.weather_dependent,
        "not_suitable_for": activity.not_suitable_for,
        "what_to_bring": activity.what_to_bring,
        "has_covid_measures": activity.has_covid_measures,
        "covid_measures": activity.covid_measures,
        "is_giftable": activity.is_giftable,
        "allows_reserve_now_pay_later": activity.allows_reserve_now_pay_later,
        "reserve_payment_deadline_hours": activity.reserve_payment_deadline_hours,
        # New relationships
        "timelines": timelines,
        "time_slots": time_slots,
        "pricing_tiers": pricing_tiers,
        "add_ons": add_ons
    }

    return ActivityDetailResponse(**response_dict)


@router.get("/{activity_id}", response_model=ActivityDetailResponse)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_optional_current_user)
):
    """Get activity details by ID."""
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.is_active == True
    ).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    return _get_activity_details(activity, db)


@router.get("/slug/{slug}", response_model=ActivityDetailResponse)
def get_activity_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_optional_current_user)
):
    """Get activity details by slug."""
    activity = db.query(Activity).filter(
        Activity.slug == slug,
        Activity.is_active == True
    ).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    return _get_activity_details(activity, db)


@router.get("/{activity_id}/similar", response_model=List[ActivityResponse])
def get_similar_activities(
    activity_id: int,
    limit: int = Query(4, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """Get similar activities based on category and destination."""
    # Get the activity
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Get activity's categories and destinations
    category_ids = db.query(ActivityCategory.category_id).filter(
        ActivityCategory.activity_id == activity_id
    ).subquery()

    destination_ids = db.query(ActivityDestination.destination_id).filter(
        ActivityDestination.activity_id == activity_id
    ).subquery()

    # Find similar activities
    query = db.query(Activity).filter(
        Activity.id != activity_id,
        Activity.is_active == True
    )

    # Join and filter by same categories or destinations
    similar_activities = (
        query.join(ActivityCategory)
        .filter(ActivityCategory.category_id.in_(category_ids))
        .union(
            query.join(ActivityDestination)
            .filter(ActivityDestination.destination_id.in_(destination_ids))
        )
    ).limit(limit).all()

    # Prepare response
    response_activities = []
    for act in similar_activities[:limit]:
        primary_image = db.query(ActivityImage).filter(
            ActivityImage.activity_id == act.id,
            ActivityImage.is_primary == True
        ).first()

        categories = db.query(Category).join(ActivityCategory).filter(
            ActivityCategory.activity_id == act.id
        ).all()

        destinations = db.query(Destination).join(ActivityDestination).filter(
            ActivityDestination.activity_id == act.id
        ).all()

        activity_dict = {
            "id": act.id,
            "title": act.title,
            "slug": act.slug,
            "short_description": act.short_description,
            "price_adult": act.price_adult,
            "price_child": act.price_child,
            "duration_minutes": act.duration_minutes,
            "average_rating": float(act.average_rating) if act.average_rating else 0,
            "total_reviews": act.total_reviews,
            "is_bestseller": act.is_bestseller,
            "is_skip_the_line": act.is_skip_the_line,
            "is_active": act.is_active,
            "free_cancellation_hours": act.free_cancellation_hours,
            "languages": act.languages,
            "primary_image": primary_image,
            "categories": categories,
            "destinations": destinations
        }
        response_activities.append(ActivityResponse(**activity_dict))

    return response_activities


@router.post("", response_model=ActivityDetailResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    activity_data: ActivityCreate,
    db: Session = Depends(get_db),
    current_vendor = Depends(get_current_vendor)
):
    """Create a new activity (vendor only)."""
    # Get vendor record from user
    vendor = db.query(Vendor).filter(Vendor.user_id == current_vendor.id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vendor profile not found"
        )

    # Create activity
    activity = Activity(
        vendor_id=vendor.id,
        title=activity_data.title,
        slug=slugify(activity_data.title),
        short_description=activity_data.short_description,
        description=activity_data.description,
        price_adult=activity_data.price_adult,
        price_child=activity_data.price_child,
        duration_minutes=activity_data.duration_minutes,
        max_group_size=activity_data.max_group_size,
        instant_confirmation=activity_data.instant_confirmation,
        free_cancellation_hours=activity_data.free_cancellation_hours,
        languages=activity_data.languages,
        is_bestseller=activity_data.is_bestseller,
        is_skip_the_line=activity_data.is_skip_the_line,
        is_active=True,
        # New enhanced fields
        has_multiple_tiers=activity_data.has_multiple_tiers,
        discount_percentage=activity_data.discount_percentage,
        original_price_adult=activity_data.original_price_adult,
        original_price_child=activity_data.original_price_child,
        is_likely_to_sell_out=activity_data.is_likely_to_sell_out,
        has_mobile_ticket=activity_data.has_mobile_ticket,
        has_best_price_guarantee=activity_data.has_best_price_guarantee,
        is_verified_activity=activity_data.is_verified_activity,
        response_time_hours=activity_data.response_time_hours,
        is_wheelchair_accessible=activity_data.is_wheelchair_accessible,
        is_stroller_accessible=activity_data.is_stroller_accessible,
        allows_service_animals=activity_data.allows_service_animals,
        has_infant_seats=activity_data.has_infant_seats,
        video_url=activity_data.video_url,
        dress_code=activity_data.dress_code,
        weather_dependent=activity_data.weather_dependent,
        not_suitable_for=activity_data.not_suitable_for,
        what_to_bring=activity_data.what_to_bring,
        has_covid_measures=activity_data.has_covid_measures,
        covid_measures=activity_data.covid_measures,
        is_giftable=activity_data.is_giftable,
        allows_reserve_now_pay_later=activity_data.allows_reserve_now_pay_later,
        reserve_payment_deadline_hours=activity_data.reserve_payment_deadline_hours
    )
    db.add(activity)
    db.flush()

    # Add categories
    for category_id in activity_data.category_ids:
        db.add(ActivityCategory(activity_id=activity.id, category_id=category_id))

    # Add destinations
    for destination_id in activity_data.destination_ids:
        db.add(ActivityDestination(activity_id=activity.id, destination_id=destination_id))

    # Add images
    for idx, img_data in enumerate(activity_data.images):
        db.add(ActivityImage(
            activity_id=activity.id,
            url=img_data['url'],
            alt_text=img_data.get('alt_text'),
            is_primary=(idx == 0),
            order_index=idx
        ))

    # Add highlights
    for idx, highlight_text in enumerate(activity_data.highlights):
        db.add(ActivityHighlight(
            activity_id=activity.id,
            text=highlight_text,
            order_index=idx
        ))

    # Add includes/excludes
    for idx, include_data in enumerate(activity_data.includes):
        db.add(ActivityInclude(
            activity_id=activity.id,
            item=include_data['item'],
            is_included=include_data['is_included'],
            order_index=idx
        ))

    # Add FAQs
    for idx, faq_data in enumerate(activity_data.faqs):
        db.add(ActivityFAQ(
            activity_id=activity.id,
            question=faq_data['question'],
            answer=faq_data['answer'],
            order_index=idx
        ))

    # Add meeting point
    if activity_data.meeting_point:
        mp = activity_data.meeting_point
        db.add(MeetingPoint(
            activity_id=activity.id,
            address=mp['address'],
            instructions=mp.get('instructions'),
            latitude=mp.get('latitude'),
            longitude=mp.get('longitude')
        ))

    db.commit()
    db.refresh(activity)

    return _get_activity_details(activity, db)


@router.put("/{activity_id}", response_model=ActivityDetailResponse)
def update_activity(
    activity_id: int,
    activity_data: ActivityUpdate,
    db: Session = Depends(get_db),
    current_vendor = Depends(get_current_vendor)
):
    """Update an activity (vendor only)."""
    # Get vendor record from user
    vendor = db.query(Vendor).filter(Vendor.user_id == current_vendor.id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vendor profile not found"
        )

    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    if activity.vendor_id != vendor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this activity"
        )

    # Update fields
    update_data = activity_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(activity, field, value)

    # Update slug if title changed
    if activity_data.title:
        activity.slug = slugify(activity_data.title)

    db.commit()
    db.refresh(activity)

    return _get_activity_details(activity, db)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_vendor = Depends(get_current_vendor)
):
    """Delete an activity (vendor only). Actually just marks as inactive."""
    # Get vendor record from user
    vendor = db.query(Vendor).filter(Vendor.user_id == current_vendor.id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vendor profile not found"
        )

    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    if activity.vendor_id != vendor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this activity"
        )

    # Soft delete - mark as inactive
    activity.is_active = False
    db.commit()

    return None


@router.patch("/{activity_id}/toggle-status", response_model=ActivityDetailResponse)
def toggle_activity_status(
    activity_id: int,
    db: Session = Depends(get_db),
    current_vendor = Depends(get_current_vendor)
):
    """Toggle activity active/inactive status (vendor only)."""
    # Get vendor record from user
    vendor = db.query(Vendor).filter(Vendor.user_id == current_vendor.id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vendor profile not found"
        )

    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    if activity.vendor_id != vendor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this activity"
        )

    # Toggle the status
    activity.is_active = not activity.is_active
    db.commit()
    db.refresh(activity)

    return _get_activity_details(activity, db)