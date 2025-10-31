"""Booking related schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime, date, time
from decimal import Decimal

from app.models.booking import BookingStatus


class BookingCreate(BaseModel):
    """Booking creation schema."""
    activity_id: int
    booking_date: date
    booking_time: Optional[time] = None
    adults: int = Field(1, ge=1)
    children: int = Field(0, ge=0)
    customer_name: Optional[str] = Field(None, max_length=255)
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = Field(None, max_length=50)
    special_requirements: Optional[str] = None

    @validator('booking_date')
    def validate_booking_date(cls, v):
        if v < date.today():
            raise ValueError('Booking date cannot be in the past')
        return v


class BookingUpdate(BaseModel):
    """Booking update schema."""
    booking_date: Optional[date] = None
    booking_time: Optional[time] = None
    adults: Optional[int] = Field(None, ge=1)
    children: Optional[int] = Field(None, ge=0)
    special_requirements: Optional[str] = None
    status: Optional[BookingStatus] = None


class BookingResponse(BaseModel):
    """Booking response schema."""
    id: int
    booking_ref: str
    activity: dict
    booking_date: date
    booking_time: Optional[time]
    adults: int
    children: int
    total_participants: int
    total_price: Decimal
    currency: str
    status: BookingStatus
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_phone: Optional[str]
    special_requirements: Optional[str]
    created_at: datetime
    confirmed_at: Optional[datetime]

    class Config:
        from_attributes = True


class AvailabilityCreate(BaseModel):
    """Availability creation schema."""
    activity_id: int
    date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    spots_total: int = Field(..., ge=1)
    price_adult: Optional[Decimal] = Field(None, ge=0)
    price_child: Optional[Decimal] = Field(None, ge=0)


class AvailabilityResponse(BaseModel):
    """Availability response schema."""
    id: int
    date: date
    start_time: Optional[time]
    end_time: Optional[time]
    spots_available: int
    spots_total: int
    price_adult: Optional[Decimal]
    price_child: Optional[Decimal]
    is_available: bool

    class Config:
        from_attributes = True


class CartItemCreate(BaseModel):
    """Cart item creation schema."""
    activity_id: int
    booking_date: date
    booking_time: Optional[time] = None
    adults: int = Field(1, ge=1)
    children: int = Field(0, ge=0)

    # Enhanced booking fields (optional)
    time_slot_id: Optional[int] = None
    pricing_tier_id: Optional[int] = None
    add_on_ids: Optional[List[int]] = None
    add_on_quantities: Optional[dict] = None  # {add_on_id: quantity}


class CartItemResponse(BaseModel):
    """Cart item response schema."""
    id: int
    activity: dict
    booking_date: date
    booking_time: Optional[time]
    adults: int
    children: int
    price: Decimal
    created_at: datetime

    class Config:
        from_attributes = True