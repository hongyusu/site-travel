"""Cart endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from decimal import Decimal
import uuid
import json

from app.database import get_db
from app.models import CartItem, Activity, ActivityImage, ActivityTimeSlot, ActivityPricingTier, ActivityAddOn
from app.schemas.booking import CartItemCreate, CartItemResponse
from app.schemas.common import MessageResponse

router = APIRouter()


def get_session_id(session_id: str = Header(None, alias="X-Session-ID")) -> str:
    """Get or create session ID for cart."""
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


def calculate_cart_price(
    db: Session,
    activity: Activity,
    adults: int,
    children: int,
    pricing_tier_id: int = None,
    time_slot_id: int = None,
    add_on_ids: List[int] = None,
    add_on_quantities: dict = None
) -> Decimal:
    """Calculate total price for cart item with enhanced booking options."""
    # Start with base prices
    base_adult_price = Decimal(str(activity.price_adult))
    base_child_price = Decimal(str(activity.price_child or 0))

    # Apply pricing tier if selected
    if pricing_tier_id:
        tier = db.query(ActivityPricingTier).filter(
            ActivityPricingTier.id == pricing_tier_id,
            ActivityPricingTier.activity_id == activity.id
        ).first()
        if tier:
            base_adult_price = tier.price_adult
            base_child_price = tier.price_child or base_child_price

    # Apply time slot price adjustment if selected
    if time_slot_id:
        slot = db.query(ActivityTimeSlot).filter(
            ActivityTimeSlot.id == time_slot_id,
            ActivityTimeSlot.activity_id == activity.id
        ).first()
        if slot and slot.price_adjustment:
            base_adult_price += slot.price_adjustment
            base_child_price += slot.price_adjustment

    # Calculate participant costs
    total = (base_adult_price * adults) + (base_child_price * children)

    # Add add-ons
    if add_on_ids and add_on_quantities:
        add_ons = db.query(ActivityAddOn).filter(
            ActivityAddOn.id.in_(add_on_ids),
            ActivityAddOn.activity_id == activity.id
        ).all()

        for add_on in add_ons:
            quantity = add_on_quantities.get(str(add_on.id), 0)
            total += add_on.price * quantity

    return total


@router.get("/", response_model=List[CartItemResponse])
def get_cart_items(
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id)
):
    """Get cart items for current session."""
    cart_items = db.query(CartItem).filter(
        CartItem.session_id == session_id
    ).order_by(CartItem.created_at.desc()).all()

    response_items = []
    for item in cart_items:
        activity = db.query(Activity).filter(Activity.id == item.activity_id).first()
        if activity:
            primary_image = db.query(ActivityImage).filter(
                ActivityImage.activity_id == activity.id,
                ActivityImage.is_primary == True
            ).first()

            activity_info = {
                "id": activity.id,
                "title": activity.title,
                "slug": activity.slug,
                "primary_image": primary_image.url if primary_image else None,
                "duration_minutes": activity.duration_minutes,
                "price_adult": activity.price_adult,
                "price_child": activity.price_child
            }

            response_items.append(CartItemResponse(
                id=item.id,
                activity=activity_info,
                booking_date=item.booking_date,
                booking_time=item.booking_time,
                adults=item.adults,
                children=item.children,
                price=item.price,
                created_at=item.created_at
            ))

    return response_items


@router.post("/add", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id)
):
    """Add item to cart."""
    # Validate activity
    activity = db.query(Activity).filter(
        Activity.id == cart_item.activity_id,
        Activity.is_active == True
    ).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Validate booking date
    if cart_item.booking_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot book for past dates"
        )

    # Check if similar item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.session_id == session_id,
        CartItem.activity_id == cart_item.activity_id,
        CartItem.booking_date == cart_item.booking_date,
        CartItem.booking_time == cart_item.booking_time
    ).first()

    # Calculate price with enhanced booking options
    total_price = calculate_cart_price(
        db=db,
        activity=activity,
        adults=cart_item.adults,
        children=cart_item.children,
        pricing_tier_id=cart_item.pricing_tier_id,
        time_slot_id=cart_item.time_slot_id,
        add_on_ids=cart_item.add_on_ids,
        add_on_quantities=cart_item.add_on_quantities
    )

    if existing_item:
        # Update quantities and enhanced booking fields
        existing_item.adults = cart_item.adults
        existing_item.children = cart_item.children
        existing_item.price = total_price
        existing_item.time_slot_id = cart_item.time_slot_id
        existing_item.pricing_tier_id = cart_item.pricing_tier_id
        existing_item.add_on_ids = json.dumps(cart_item.add_on_ids) if cart_item.add_on_ids else None
        existing_item.add_on_quantities = json.dumps(cart_item.add_on_quantities) if cart_item.add_on_quantities else None
        db.commit()
        db.refresh(existing_item)
        db_cart_item = existing_item
    else:
        # Create new cart item
        db_cart_item = CartItem(
            session_id=session_id,
            activity_id=cart_item.activity_id,
            booking_date=cart_item.booking_date,
            booking_time=cart_item.booking_time,
            adults=cart_item.adults,
            children=cart_item.children,
            price=total_price,
            time_slot_id=cart_item.time_slot_id,
            pricing_tier_id=cart_item.pricing_tier_id,
            add_on_ids=json.dumps(cart_item.add_on_ids) if cart_item.add_on_ids else None,
            add_on_quantities=json.dumps(cart_item.add_on_quantities) if cart_item.add_on_quantities else None
        )

        db.add(db_cart_item)
        db.commit()
        db.refresh(db_cart_item)

    # Prepare response
    primary_image = db.query(ActivityImage).filter(
        ActivityImage.activity_id == activity.id,
        ActivityImage.is_primary == True
    ).first()

    activity_info = {
        "id": activity.id,
        "title": activity.title,
        "slug": activity.slug,
        "primary_image": primary_image.url if primary_image else None,
        "duration_minutes": activity.duration_minutes,
        "price_adult": activity.price_adult,
        "price_child": activity.price_child
    }

    return CartItemResponse(
        id=db_cart_item.id,
        activity=activity_info,
        booking_date=db_cart_item.booking_date,
        booking_time=db_cart_item.booking_time,
        adults=db_cart_item.adults,
        children=db_cart_item.children,
        price=db_cart_item.price,
        created_at=db_cart_item.created_at
    )


@router.put("/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    cart_update: CartItemCreate,
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id)
):
    """Update cart item quantities."""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.session_id == session_id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    activity = db.query(Activity).filter(Activity.id == cart_item.activity_id).first()

    # Recalculate price with enhanced booking options
    total_price = calculate_cart_price(
        db=db,
        activity=activity,
        adults=cart_update.adults,
        children=cart_update.children,
        pricing_tier_id=cart_update.pricing_tier_id,
        time_slot_id=cart_update.time_slot_id,
        add_on_ids=cart_update.add_on_ids,
        add_on_quantities=cart_update.add_on_quantities
    )

    # Update quantities and enhanced booking fields
    cart_item.adults = cart_update.adults
    cart_item.children = cart_update.children
    cart_item.booking_date = cart_update.booking_date
    cart_item.booking_time = cart_update.booking_time
    cart_item.price = total_price
    cart_item.time_slot_id = cart_update.time_slot_id
    cart_item.pricing_tier_id = cart_update.pricing_tier_id
    cart_item.add_on_ids = json.dumps(cart_update.add_on_ids) if cart_update.add_on_ids else None
    cart_item.add_on_quantities = json.dumps(cart_update.add_on_quantities) if cart_update.add_on_quantities else None

    db.commit()
    db.refresh(cart_item)

    # Prepare response
    primary_image = db.query(ActivityImage).filter(
        ActivityImage.activity_id == activity.id,
        ActivityImage.is_primary == True
    ).first()

    activity_info = {
        "id": activity.id,
        "title": activity.title,
        "slug": activity.slug,
        "primary_image": primary_image.url if primary_image else None,
        "duration_minutes": activity.duration_minutes,
        "price_adult": activity.price_adult,
        "price_child": activity.price_child
    }

    return CartItemResponse(
        id=cart_item.id,
        activity=activity_info,
        booking_date=cart_item.booking_date,
        booking_time=cart_item.booking_time,
        adults=cart_item.adults,
        children=cart_item.children,
        price=cart_item.price,
        created_at=cart_item.created_at
    )


@router.delete("/{item_id}", response_model=MessageResponse)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id)
):
    """Remove item from cart."""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.session_id == session_id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    db.delete(cart_item)
    db.commit()

    return MessageResponse(message="Item removed from cart")


@router.delete("/", response_model=MessageResponse)
def clear_cart(
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id)
):
    """Clear all items from cart."""
    db.query(CartItem).filter(CartItem.session_id == session_id).delete()
    db.commit()

    return MessageResponse(message="Cart cleared")


@router.get("/total", response_model=dict)
def get_cart_total(
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id)
):
    """Get cart total."""
    cart_items = db.query(CartItem).filter(CartItem.session_id == session_id).all()

    total = Decimal(0)
    item_count = 0

    for item in cart_items:
        total += item.price
        item_count += 1

    return {
        "item_count": item_count,
        "total": float(total),
        "currency": "EUR",
        "session_id": session_id
    }