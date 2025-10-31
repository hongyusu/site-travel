"""Review related schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ReviewCreate(BaseModel):
    """Review creation schema."""
    activity_id: int
    booking_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=255)
    comment: Optional[str] = None


class ReviewUpdate(BaseModel):
    """Review update schema."""
    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, max_length=255)
    comment: Optional[str] = None


class ReviewImageResponse(BaseModel):
    """Review image response."""
    id: int
    url: str
    caption: Optional[str]

    class Config:
        from_attributes = True


class ReviewCategoryResponse(BaseModel):
    """Review category rating response."""
    id: int
    category_name: str
    rating: int

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    """Review response schema."""
    id: int
    user: dict
    rating: int
    title: Optional[str]
    comment: Optional[str]
    is_verified_booking: bool
    helpful_count: int
    created_at: datetime
    images: List[ReviewImageResponse] = []
    category_ratings: List[ReviewCategoryResponse] = []

    class Config:
        from_attributes = True