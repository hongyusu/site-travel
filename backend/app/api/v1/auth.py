"""Authentication endpoints."""

import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

from app.database import get_db
from app.models.user import User, UserRole, Vendor
from app.models import Booking, Review, Wishlist
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
    VendorCreate,
    VendorRegister
)
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token
)
from app.config import settings
from app.api.deps import get_current_user, get_current_active_user
from app.services.email import EmailService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        UserResponse: Created user

    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    db_user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        phone=user_data.phone,
        role=UserRole.CUSTOMER
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Send welcome email
        try:
            EmailService.send_welcome_email(
                user_email=db_user.email,
                user_name=db_user.full_name
            )
        except Exception as e:
            # Log email error but don't fail registration
            logger.error(f"Failed to send welcome email to {db_user.email}: {e}")
            
    except IntegrityError as e:
        db.rollback()
        logger.error(f"IntegrityError during user creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during user creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user"
        )

    return db_user


@router.post("/register-vendor", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_vendor(
    data: VendorRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new vendor.

    Args:
        data: Combined vendor registration data
        db: Database session

    Returns:
        UserResponse: Created vendor user

    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user with vendor role
    db_user = User(
        email=data.email,
        password_hash=get_password_hash(data.password),
        full_name=data.full_name,
        phone=data.phone,
        role=UserRole.VENDOR
    )

    try:
        db.add(db_user)
        db.flush()  # Get user ID without committing

        # Create vendor profile
        db_vendor = Vendor(
            user_id=db_user.id,
            company_name=data.company_name,
            description=None,
            logo_url=None,
            commission_rate=settings.DEFAULT_COMMISSION_RATE
        )
        db.add(db_vendor)

        db.commit()
        db.refresh(db_user)
        
        # Send vendor welcome email
        try:
            EmailService.send_vendor_welcome_email(
                user_email=db_user.email,
                user_name=db_user.full_name,
                company_name=data.company_name
            )
        except Exception as e:
            # Log email error but don't fail registration
            logger.error(f"Failed to send vendor welcome email to {db_user.email}: {e}")
            
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create vendor"
        )

    return db_user


@router.post("/login", response_model=Token)
def login(
    form_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login user and return access token.

    Args:
        form_data: Login credentials
        db: Database session

    Returns:
        Token: Access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Create tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user profile.

    Args:
        current_user: Current authenticated user

    Returns:
        UserResponse: Current user profile
    """
    return current_user


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.

    Args:
        refresh_token: Refresh token
        db: Database session

    Returns:
        Token: New access and refresh tokens

    Raises:
        HTTPException: If refresh token is invalid
    """
    from app.core.security import decode_token
    from app.schemas.user import TokenPayload

    try:
        payload = decode_token(refresh_token)
        token_data = TokenPayload(**payload)

        if token_data.type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user = db.query(User).filter(User.id == int(token_data.sub)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Create new tokens
    access_token = create_access_token(subject=str(user.id))
    new_refresh_token = create_refresh_token(subject=str(user.id))

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token
    )


@router.get("/me/statistics")
def get_user_statistics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's statistics.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        dict: User statistics including bookings, wishlist items, and reviews counts
    """
    # Count bookings
    total_bookings = db.query(Booking).filter(Booking.user_id == current_user.id).count()
    
    # Count wishlist items
    wishlist_items = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).count()
    
    # Count reviews
    reviews = db.query(Review).filter(Review.user_id == current_user.id).count()
    
    return {
        "total_bookings": total_bookings,
        "wishlist_items": wishlist_items,
        "reviews": reviews
    }