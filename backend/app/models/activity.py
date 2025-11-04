"""Activity related models."""

from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, DateTime, Text, ARRAY, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Category(Base):
    """Category model."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    icon = Column(String(50))
    parent_id = Column(Integer, ForeignKey("categories.id"))
    order_index = Column(Integer, default=0)

    # Relationships
    activities = relationship("ActivityCategory", back_populates="category")
    children = relationship("Category", backref="parent", remote_side=[id])
    translations = relationship("CategoryTranslation", back_populates="category")


class Destination(Base):
    """Destination model."""

    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    country = Column(String(100))
    country_code = Column(String(2))
    image_url = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    activities = relationship("ActivityDestination", back_populates="destination")
    translations = relationship("DestinationTranslation", back_populates="destination")


class Activity(Base):
    """Activity model."""

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False, index=True)
    description = Column(Text)
    short_description = Column(Text)
    price_adult = Column(DECIMAL(10, 2), nullable=False)
    price_child = Column(DECIMAL(10, 2))
    price_currency = Column(String(3), default="EUR")
    duration_minutes = Column(Integer)
    max_group_size = Column(Integer)
    instant_confirmation = Column(Boolean, default=True)
    free_cancellation_hours = Column(Integer, default=24)
    languages = Column(ARRAY(String), default=[])
    is_bestseller = Column(Boolean, default=False)
    is_skip_the_line = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Pricing variations
    has_multiple_tiers = Column(Boolean, default=False)
    discount_percentage = Column(Integer)
    original_price_adult = Column(DECIMAL(10, 2))
    original_price_child = Column(DECIMAL(10, 2))

    # Features & badges
    is_likely_to_sell_out = Column(Boolean, default=False)
    has_mobile_ticket = Column(Boolean, default=False)
    has_best_price_guarantee = Column(Boolean, default=False)
    is_verified_activity = Column(Boolean, default=False)
    response_time_hours = Column(Integer, default=24)

    # Accessibility
    is_wheelchair_accessible = Column(Boolean, default=False)
    is_stroller_accessible = Column(Boolean, default=False)
    allows_service_animals = Column(Boolean, default=False)
    has_infant_seats = Column(Boolean, default=False)

    # Additional info
    video_url = Column(String(500))
    dress_code = Column(Text)
    weather_dependent = Column(Boolean, default=False)
    not_suitable_for = Column(Text)
    what_to_bring = Column(Text)

    # COVID-19
    has_covid_measures = Column(Boolean, default=False)
    covid_measures = Column(Text)

    # Booking options
    is_giftable = Column(Boolean, default=False)
    allows_reserve_now_pay_later = Column(Boolean, default=False)
    reserve_payment_deadline_hours = Column(Integer, default=24)

    # Computed fields
    average_rating = Column(DECIMAL(2, 1), default=0)
    total_reviews = Column(Integer, default=0)
    total_bookings = Column(Integer, default=0)

    # Relationships
    vendor = relationship("Vendor", back_populates="activities")
    images = relationship("ActivityImage", back_populates="activity", cascade="all, delete-orphan")
    categories = relationship("ActivityCategory", back_populates="activity", cascade="all, delete-orphan")
    destinations = relationship("ActivityDestination", back_populates="activity", cascade="all, delete-orphan")
    highlights = relationship("ActivityHighlight", back_populates="activity", cascade="all, delete-orphan")
    includes = relationship("ActivityInclude", back_populates="activity", cascade="all, delete-orphan")
    faqs = relationship("ActivityFAQ", back_populates="activity", cascade="all, delete-orphan")
    meeting_point = relationship("MeetingPoint", back_populates="activity", uselist=False, cascade="all, delete-orphan")
    availability = relationship("Availability", back_populates="activity", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="activity")
    reviews = relationship("Review", back_populates="activity")
    wishlist_items = relationship("Wishlist", back_populates="activity", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="activity", cascade="all, delete-orphan")

    # New relationships
    timelines = relationship("ActivityTimeline", back_populates="activity", cascade="all, delete-orphan")
    time_slots = relationship("ActivityTimeSlot", back_populates="activity", cascade="all, delete-orphan")
    pricing_tiers = relationship("ActivityPricingTier", back_populates="activity", cascade="all, delete-orphan")
    add_ons = relationship("ActivityAddOn", back_populates="activity", cascade="all, delete-orphan")

    # Translation relationships
    translations = relationship("ActivityTranslation", back_populates="activity", cascade="all, delete-orphan")


class ActivityImage(Base):
    """Activity image model."""

    __tablename__ = "activity_images"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    caption = Column(Text)
    is_primary = Column(Boolean, default=False)
    is_hero = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)

    # Relationships
    activity = relationship("Activity", back_populates="images")


class ActivityCategory(Base):
    """Activity-Category many-to-many relationship."""

    __tablename__ = "activity_categories"

    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    activity = relationship("Activity", back_populates="categories")
    category = relationship("Category", back_populates="activities")


class ActivityDestination(Base):
    """Activity-Destination many-to-many relationship."""

    __tablename__ = "activity_destinations"

    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    activity = relationship("Activity", back_populates="destinations")
    destination = relationship("Destination", back_populates="activities")


class ActivityHighlight(Base):
    """Activity highlight model."""

    __tablename__ = "activity_highlights"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    text = Column(String(500), nullable=False)
    order_index = Column(Integer, default=0)

    # Relationships
    activity = relationship("Activity", back_populates="highlights")
    translations = relationship("ActivityHighlightTranslation", back_populates="highlight", cascade="all, delete-orphan")


class ActivityInclude(Base):
    """Activity includes/excludes model."""

    __tablename__ = "activity_includes"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    item = Column(String(500), nullable=False)
    is_included = Column(Boolean, default=True)  # True for included, False for excluded
    order_index = Column(Integer, default=0)

    # Relationships
    activity = relationship("Activity", back_populates="includes")
    translations = relationship("ActivityIncludeTranslation", back_populates="include_item", cascade="all, delete-orphan")


class ActivityFAQ(Base):
    """Activity FAQ model."""

    __tablename__ = "activity_faqs"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)

    # Relationships
    activity = relationship("Activity", back_populates="faqs")
    translations = relationship("ActivityFAQTranslation", back_populates="faq", cascade="all, delete-orphan")


class MeetingPoint(Base):
    """Meeting point model."""

    __tablename__ = "meeting_points"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, unique=True)
    address = Column(Text, nullable=False)
    instructions = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    parking_info = Column(Text)
    public_transport_info = Column(Text)
    nearby_landmarks = Column(Text)

    # Relationships
    activity = relationship("Activity", back_populates="meeting_point")
    photos = relationship("MeetingPointPhoto", back_populates="meeting_point", cascade="all, delete-orphan")
    translations = relationship("MeetingPointTranslation", back_populates="meeting_point", cascade="all, delete-orphan")


class ActivityTimeline(Base):
    """Activity timeline/itinerary model."""

    __tablename__ = "activity_timelines"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer)
    image_url = Column(String(500))
    order_index = Column(Integer, default=0)

    # Relationships
    activity = relationship("Activity", back_populates="timelines")
    translations = relationship("ActivityTimelineTranslation", back_populates="timeline", cascade="all, delete-orphan")


class ActivityTimeSlot(Base):
    """Activity time slot model."""

    __tablename__ = "activity_time_slots"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    slot_time = Column(String(5), nullable=False)  # HH:MM format
    slot_label = Column(String(50))  # "Morning", "Afternoon", "Evening"
    max_capacity = Column(Integer)
    is_available = Column(Boolean, default=True)
    price_adjustment = Column(DECIMAL(10, 2), default=0)

    # Relationships
    activity = relationship("Activity", back_populates="time_slots")


class ActivityPricingTier(Base):
    """Activity pricing tier model."""

    __tablename__ = "activity_pricing_tiers"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    tier_name = Column(String(100), nullable=False)  # "Standard", "Premium", "VIP"
    tier_description = Column(Text)
    price_adult = Column(DECIMAL(10, 2), nullable=False)
    price_child = Column(DECIMAL(10, 2))
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    # Relationships
    activity = relationship("Activity", back_populates="pricing_tiers")
    translations = relationship("ActivityPricingTierTranslation", back_populates="pricing_tier", cascade="all, delete-orphan")


class ActivityAddOn(Base):
    """Activity add-on model."""

    __tablename__ = "activity_add_ons"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    is_optional = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)

    # Relationships
    activity = relationship("Activity", back_populates="add_ons")
    translations = relationship("ActivityAddOnTranslation", back_populates="addon", cascade="all, delete-orphan")


class MeetingPointPhoto(Base):
    """Meeting point photo model."""

    __tablename__ = "meeting_point_photos"

    id = Column(Integer, primary_key=True, index=True)
    meeting_point_id = Column(Integer, ForeignKey("meeting_points.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(500), nullable=False)
    caption = Column(String(255))
    order_index = Column(Integer, default=0)

    # Relationships
    meeting_point = relationship("MeetingPoint", back_populates="photos")