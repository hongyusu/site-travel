"""Pydantic schemas for request/response validation."""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserInDB,
    UserResponse,
    UserLogin,
    Token,
    TokenPayload,
    VendorCreate,
    VendorResponse
)

from app.schemas.activity import (
    ActivityBase,
    ActivityCreate,
    ActivityUpdate,
    ActivityResponse,
    ActivityDetailResponse,
    CategoryResponse,
    DestinationResponse,
    ActivitySearchParams
)

from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingResponse,
    AvailabilityResponse,
    CartItemCreate,
    CartItemResponse
)

from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse
)

from app.schemas.common import (
    PaginationParams,
    PaginatedResponse,
    MessageResponse
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenPayload",
    "VendorCreate",
    "VendorResponse",

    # Activity schemas
    "ActivityBase",
    "ActivityCreate",
    "ActivityUpdate",
    "ActivityResponse",
    "ActivityDetailResponse",
    "CategoryResponse",
    "DestinationResponse",
    "ActivitySearchParams",

    # Booking schemas
    "BookingCreate",
    "BookingUpdate",
    "BookingResponse",
    "AvailabilityResponse",
    "CartItemCreate",
    "CartItemResponse",

    # Review schemas
    "ReviewCreate",
    "ReviewUpdate",
    "ReviewResponse",

    # Common schemas
    "PaginationParams",
    "PaginatedResponse",
    "MessageResponse",
]