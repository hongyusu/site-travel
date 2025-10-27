"""User related schemas."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class UserUpdate(BaseModel):
    """User update schema."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)


class UserInDB(UserBase):
    """User in database schema."""
    id: int
    role: UserRole
    email_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """User response schema."""
    id: int
    role: UserRole
    email_verified: bool
    created_at: datetime
    vendor_profile: Optional["VendorResponse"] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: str
    exp: int
    type: str


class VendorCreate(BaseModel):
    """Vendor creation schema."""
    company_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    logo_url: Optional[str] = Field(None, max_length=500)


class VendorResponse(BaseModel):
    """Vendor response schema."""
    id: int
    company_name: str
    description: Optional[str]
    logo_url: Optional[str]
    is_verified: bool
    commission_rate: float
    created_at: datetime

    class Config:
        from_attributes = True


# Resolve forward references
UserResponse.model_rebuild()