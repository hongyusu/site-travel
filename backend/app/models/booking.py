"""Booking related models."""

from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, DateTime, Date, Time, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import random
import string

from app.database import Base


class BookingStatus(str, enum.Enum):
    """Booking status enumeration."""
    PENDING = "pending"
    PENDING_VENDOR_APPROVAL = "pending_vendor_approval"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


def generate_booking_ref():
    """Generate unique booking reference."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


class Booking(Base):
    """Booking model."""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_ref = Column(String(20), unique=True, nullable=False, default=generate_booking_ref, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False)

    # Booking details
    booking_date = Column(Date, nullable=False)
    booking_time = Column(Time)
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    total_participants = Column(Integer, nullable=False)

    # Pricing
    price_per_adult = Column(DECIMAL(10, 2))
    price_per_child = Column(DECIMAL(10, 2))
    total_price = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="EUR")

    # Status
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING, nullable=False)

    # Customer details (for guest checkout)
    customer_name = Column(String(255))
    customer_email = Column(String(255))
    customer_phone = Column(String(50))
    special_requirements = Column(Text)

    # Vendor management
    rejection_reason = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    confirmed_at = Column(DateTime(timezone=True))
    vendor_approved_at = Column(DateTime(timezone=True))
    vendor_rejected_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="bookings")
    activity = relationship("Activity", back_populates="bookings")
    vendor = relationship("Vendor", back_populates="bookings")
    review = relationship("Review", back_populates="booking", uselist=False)

    # Indexes
    __table_args__ = (
        Index('idx_booking_date', 'booking_date'),
        Index('idx_user_bookings', 'user_id', 'status'),
        Index('idx_vendor_bookings', 'vendor_id', 'booking_date'),
    )


class Availability(Base):
    """Availability model."""

    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time)
    end_time = Column(Time)
    spots_available = Column(Integer)
    spots_total = Column(Integer)
    price_adult = Column(DECIMAL(10, 2))
    price_child = Column(DECIMAL(10, 2))
    is_available = Column(Boolean, default=True)

    # Relationships
    activity = relationship("Activity", back_populates="availability")

    # Constraints
    __table_args__ = (
        Index('idx_availability', 'activity_id', 'date', 'start_time', unique=True),
        Index('idx_availability_date', 'date'),
    )


class CartItem(Base):
    """Cart item model."""

    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    booking_date = Column(Date, nullable=False)
    booking_time = Column(Time)
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    price = Column(DECIMAL(10, 2))

    # Enhanced booking fields
    time_slot_id = Column(Integer, ForeignKey("activity_time_slots.id", ondelete="SET NULL"))
    pricing_tier_id = Column(Integer, ForeignKey("activity_pricing_tiers.id", ondelete="SET NULL"))
    add_on_ids = Column(Text)  # JSON array of add-on IDs
    add_on_quantities = Column(Text)  # JSON object {add_on_id: quantity}

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    activity = relationship("Activity", back_populates="cart_items")

    # Indexes
    __table_args__ = (
        Index('idx_cart_session', 'session_id'),
    )