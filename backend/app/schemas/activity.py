"""Activity related schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class CategoryResponse(BaseModel):
    """Category response schema."""
    id: int
    name: str
    slug: str
    icon: Optional[str]

    class Config:
        from_attributes = True


class DestinationResponse(BaseModel):
    """Destination response schema."""
    id: int
    name: str
    slug: str
    country: Optional[str]
    image_url: Optional[str]
    is_featured: bool

    class Config:
        from_attributes = True


class ActivityImageResponse(BaseModel):
    """Activity image response schema."""
    id: int
    url: str
    alt_text: Optional[str]
    caption: Optional[str]
    is_primary: bool
    is_hero: bool

    class Config:
        from_attributes = True


class ActivityHighlightResponse(BaseModel):
    """Activity highlight response."""
    id: int
    text: str

    class Config:
        from_attributes = True


class ActivityIncludeResponse(BaseModel):
    """Activity include/exclude response."""
    id: int
    item: str
    is_included: bool

    class Config:
        from_attributes = True


class ActivityFAQResponse(BaseModel):
    """Activity FAQ response."""
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True


class MeetingPointPhotoResponse(BaseModel):
    """Meeting point photo response."""
    id: int
    url: str
    caption: Optional[str]

    class Config:
        from_attributes = True


class MeetingPointResponse(BaseModel):
    """Meeting point response."""
    id: int
    address: str
    instructions: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    parking_info: Optional[str]
    public_transport_info: Optional[str]
    nearby_landmarks: Optional[str]
    photos: List[MeetingPointPhotoResponse] = []

    class Config:
        from_attributes = True


class ActivityTimelineResponse(BaseModel):
    """Activity timeline response."""
    id: int
    step_number: int
    title: str
    description: Optional[str]
    duration_minutes: Optional[int]
    image_url: Optional[str]

    class Config:
        from_attributes = True


class ActivityTimeSlotResponse(BaseModel):
    """Activity time slot response."""
    id: int
    slot_time: str
    slot_label: Optional[str]
    max_capacity: Optional[int]
    is_available: bool
    price_adjustment: Decimal

    class Config:
        from_attributes = True


class ActivityPricingTierResponse(BaseModel):
    """Activity pricing tier response."""
    id: int
    tier_name: str
    tier_description: Optional[str]
    price_adult: Decimal
    price_child: Optional[Decimal]
    is_active: bool

    class Config:
        from_attributes = True


class ActivityAddOnResponse(BaseModel):
    """Activity add-on response."""
    id: int
    name: str
    description: Optional[str]
    price: Decimal
    is_optional: bool

    class Config:
        from_attributes = True


class ActivityBase(BaseModel):
    """Base activity schema."""
    title: str = Field(..., min_length=1, max_length=500)
    short_description: Optional[str] = None
    description: Optional[str] = None
    price_adult: Decimal = Field(..., ge=0)
    price_child: Optional[Decimal] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=0)
    max_group_size: Optional[int] = Field(None, ge=1)
    instant_confirmation: bool = True
    free_cancellation_hours: int = 24
    languages: List[str] = []
    is_bestseller: bool = False
    is_skip_the_line: bool = False

    # New fields
    has_multiple_tiers: bool = False
    discount_percentage: Optional[int] = None
    original_price_adult: Optional[Decimal] = None
    original_price_child: Optional[Decimal] = None
    is_likely_to_sell_out: bool = False
    has_mobile_ticket: bool = False
    has_best_price_guarantee: bool = False
    is_verified_activity: bool = False
    response_time_hours: int = 24
    is_wheelchair_accessible: bool = False
    is_stroller_accessible: bool = False
    allows_service_animals: bool = False
    has_infant_seats: bool = False
    video_url: Optional[str] = None
    dress_code: Optional[str] = None
    weather_dependent: bool = False
    not_suitable_for: Optional[str] = None
    what_to_bring: Optional[str] = None
    has_covid_measures: bool = False
    covid_measures: Optional[str] = None
    is_giftable: bool = False
    allows_reserve_now_pay_later: bool = False
    reserve_payment_deadline_hours: int = 24


class ActivityCreate(ActivityBase):
    """Activity creation schema."""
    category_ids: List[int] = []
    destination_ids: List[int] = []
    images: List[dict] = []
    highlights: List[str] = []
    includes: List[dict] = []  # [{"item": "...", "is_included": true/false}]
    faqs: List[dict] = []  # [{"question": "...", "answer": "..."}]
    meeting_point: Optional[dict] = None  # {"address": "...", "instructions": "...", "lat": ..., "lng": ...}


class ActivityUpdate(BaseModel):
    """Activity update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    short_description: Optional[str] = None
    description: Optional[str] = None
    price_adult: Optional[Decimal] = Field(None, ge=0)
    price_child: Optional[Decimal] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=0)
    max_group_size: Optional[int] = Field(None, ge=1)
    instant_confirmation: Optional[bool] = None
    free_cancellation_hours: Optional[int] = None
    languages: Optional[List[str]] = None
    is_bestseller: Optional[bool] = None
    is_skip_the_line: Optional[bool] = None
    is_active: Optional[bool] = None


class ActivityResponse(BaseModel):
    """Activity response schema."""
    id: int
    title: str
    slug: str
    short_description: Optional[str]
    price_adult: Decimal
    price_child: Optional[Decimal]
    duration_minutes: Optional[int]
    average_rating: float
    total_reviews: int
    is_bestseller: bool
    is_skip_the_line: bool
    is_active: bool = True
    free_cancellation_hours: int
    languages: List[str]
    primary_image: Optional[ActivityImageResponse] = None
    categories: List[CategoryResponse] = []
    destinations: List[DestinationResponse] = []

    class Config:
        from_attributes = True


class ActivityDetailResponse(ActivityResponse):
    """Detailed activity response schema."""
    description: Optional[str]
    max_group_size: Optional[int]
    instant_confirmation: bool
    total_bookings: int
    images: List[ActivityImageResponse] = []
    highlights: List[ActivityHighlightResponse] = []
    includes: List[ActivityIncludeResponse] = []
    faqs: List[ActivityFAQResponse] = []
    meeting_point: Optional[MeetingPointResponse] = None
    vendor: dict

    # New enhanced fields
    has_multiple_tiers: bool
    discount_percentage: Optional[int]
    original_price_adult: Optional[Decimal]
    original_price_child: Optional[Decimal]
    is_likely_to_sell_out: bool
    has_mobile_ticket: bool
    has_best_price_guarantee: bool
    is_verified_activity: bool
    response_time_hours: int
    is_wheelchair_accessible: bool
    is_stroller_accessible: bool
    allows_service_animals: bool
    has_infant_seats: bool
    video_url: Optional[str]
    dress_code: Optional[str]
    weather_dependent: bool
    not_suitable_for: Optional[str]
    what_to_bring: Optional[str]
    has_covid_measures: bool
    covid_measures: Optional[str]
    is_giftable: bool
    allows_reserve_now_pay_later: bool
    reserve_payment_deadline_hours: int

    # New relationships
    timelines: List[ActivityTimelineResponse] = []
    time_slots: List[ActivityTimeSlotResponse] = []
    pricing_tiers: List[ActivityPricingTierResponse] = []
    add_ons: List[ActivityAddOnResponse] = []

    class Config:
        from_attributes = True


class ActivitySearchParams(BaseModel):
    """Activity search parameters."""
    q: Optional[str] = Field(None, description="Search query")
    destination_id: Optional[int] = Field(None, description="Destination ID")
    category_ids: Optional[List[int]] = Field(None, description="Category IDs")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Maximum price")
    min_duration: Optional[int] = Field(None, ge=0, description="Minimum duration in minutes")
    max_duration: Optional[int] = Field(None, ge=0, description="Maximum duration in minutes")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    languages: Optional[List[str]] = Field(None, description="Languages")
    free_cancellation: Optional[bool] = Field(None, description="Free cancellation only")
    instant_confirmation: Optional[bool] = Field(None, description="Instant confirmation only")
    skip_the_line: Optional[bool] = Field(None, description="Skip the line only")
    sort_by: Optional[str] = Field("recommended", description="Sort by: recommended, price_asc, price_desc, rating, duration")