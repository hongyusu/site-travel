"""Stripe Checkout payment endpoints (hosted redirect flow).

Lightest integration: the backend creates a Stripe Checkout Session from the
server-validated cart and returns its hosted URL; the browser redirects there.
On return, /confirm verifies the session is paid and creates the bookings
(idempotent on the Stripe session id). Falls back gracefully (enabled=false)
when STRIPE_SECRET_KEY is unset, so the no-payment flow keeps working.
"""

import logging
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Header, Body, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.models import Booking, BookingStatus, CartItem, Activity
from app.api.deps import get_optional_current_user
from app.services.email import EmailService

logger = logging.getLogger(__name__)
router = APIRouter()


def _stripe():
    """Return the configured stripe module, or None if payments are disabled."""
    if not settings.STRIPE_SECRET_KEY:
        return None
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


def refund_booking_payment(booking) -> bool:
    """Refund a paid booking's Stripe payment. Returns True on success.

    Used when a paid booking is rejected/cancelled. Derives the PaymentIntent
    from the stored Checkout session, so no extra column is needed.
    """
    stripe = _stripe()
    if stripe is None:
        return False
    if getattr(booking, "payment_status", None) != "paid":
        return False
    sid = getattr(booking, "stripe_session_id", None)
    if not sid:
        return False
    try:
        cs = stripe.checkout.Session.retrieve(sid)
        payment_intent = cs.get("payment_intent")
        if not payment_intent:
            return False
        stripe.Refund.create(payment_intent=payment_intent)
        return True
    except Exception as e:
        logger.error(f"Refund failed for booking {getattr(booking, 'id', '?')}: {e}")
        return False


def _cents(amount) -> int:
    return int((Decimal(str(amount or 0)) * 100).to_integral_value())


@router.post("/checkout-session")
def create_checkout_session(
    payload: dict = Body(default={}),
    session_id: str = Header(None, alias="X-Session-ID"),
    db: Session = Depends(get_db),
):
    """Create a Stripe Checkout Session from the current cart; return its URL."""
    stripe = _stripe()
    if stripe is None:
        return {"enabled": False}
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing cart session")

    items = (
        db.query(CartItem)
        .filter(CartItem.session_id == session_id)
        .order_by(CartItem.created_at)
        .all()
    )
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    currency = "eur"
    line_items = []
    subtotal = Decimal("0")
    for it in items:
        activity = db.query(Activity).filter(Activity.id == it.activity_id).first()
        if not activity:
            continue
        price = Decimal(str(it.price or 0))
        subtotal += price
        line_items.append({
            "price_data": {
                "currency": currency,
                "product_data": {"name": (activity.title or "Activity")[:120]},
                "unit_amount": _cents(price),
            },
            "quantity": 1,
        })

    if not line_items:
        raise HTTPException(status_code=400, detail="Cart has no valid items")

    fee = (subtotal * Decimal(str(settings.SERVICE_FEE_RATE))).quantize(Decimal("0.01"))
    if fee > 0:
        line_items.append({
            "price_data": {
                "currency": currency,
                "product_data": {"name": "Service fee"},
                "unit_amount": _cents(fee),
            },
            "quantity": 1,
        })

    # Build success/cancel URLs from a trusted origin only (avoid open redirect).
    origin = (payload.get("origin") or "").rstrip("/")
    if origin not in settings.CORS_ORIGINS:
        origin = "https://travel.finuo.fi"

    customer_email = (payload.get("customer_email") or "").strip() or None

    try:
        cs = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url=f"{origin}/order-confirmation?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{origin}/checkout",
            customer_email=customer_email,
            # No payment_method_types set on purpose: Checkout uses the methods
            # enabled in the Stripe dashboard, so Alipay/WeChat/Klarna can be
            # turned on later with no code change.
            metadata={
                "cart_session_id": session_id,
                "customer_name": (payload.get("customer_name") or "")[:200],
                "customer_email": (payload.get("customer_email") or "")[:200],
                "customer_phone": (payload.get("customer_phone") or "")[:50],
                "special_requirements": (payload.get("special_requirements") or "")[:480],
            },
        )
    except Exception as e:
        logger.error(f"Stripe session creation failed: {e}")
        raise HTTPException(status_code=502, detail="Could not start payment")

    return {"enabled": True, "url": cs.url, "id": cs.id}


@router.post("/confirm")
def confirm_checkout(
    payload: dict = Body(default={}),
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user),
):
    """Verify a paid Checkout Session and create the bookings (idempotent)."""
    stripe = _stripe()
    if stripe is None:
        raise HTTPException(status_code=400, detail="Payments not enabled")
    sid = payload.get("session_id")
    if not sid:
        raise HTTPException(status_code=400, detail="Missing session_id")

    # Idempotency: if bookings already exist for this session, return them.
    existing = db.query(Booking).filter(Booking.stripe_session_id == sid).all()
    if existing:
        refs = [b.booking_ref for b in existing]
        return {"status": "paid", "booking_refs": refs, "first_ref": refs[0]}

    try:
        cs = stripe.checkout.Session.retrieve(sid)
    except Exception as e:
        logger.error(f"Stripe session retrieve failed: {e}")
        raise HTTPException(status_code=404, detail="Payment session not found")

    if cs.get("payment_status") != "paid":
        return {"status": cs.get("payment_status"), "booking_refs": [], "first_ref": None}

    md = cs.get("metadata") or {}
    cart_session_id = md.get("cart_session_id")
    items = (
        db.query(CartItem).filter(CartItem.session_id == cart_session_id).all()
        if cart_session_id else []
    )

    created = []
    for it in items:
        activity = db.query(Activity).filter(
            Activity.id == it.activity_id, Activity.is_active == True
        ).first()
        if not activity:
            continue
        participants = (it.adults or 0) + (it.children or 0)
        # Payment is captured now; activities without instant confirmation still
        # go through the vendor-approval queue (just already paid).
        instant = bool(activity.instant_confirmation)
        booking = Booking(
            user_id=current_user.id if current_user else None,
            activity_id=activity.id,
            vendor_id=activity.vendor_id,
            booking_date=it.booking_date,
            booking_time=it.booking_time,
            adults=it.adults or 1,
            children=it.children or 0,
            total_participants=participants or 1,
            price_per_adult=activity.price_adult,
            price_per_child=activity.price_child,
            total_price=it.price or 0,
            currency=getattr(activity, "price_currency", "EUR") or "EUR",
            status=BookingStatus.CONFIRMED if instant else BookingStatus.PENDING_VENDOR_APPROVAL,
            confirmed_at=datetime.utcnow() if instant else None,
            payment_status="paid",
            stripe_session_id=sid,
            customer_name=md.get("customer_name") or None,
            customer_email=md.get("customer_email") or None,
            customer_phone=md.get("customer_phone") or None,
            special_requirements=md.get("special_requirements") or None,
        )
        db.add(booking)
        activity.total_bookings = (activity.total_bookings or 0) + 1
        created.append((booking, activity))

    db.commit()

    refs = []
    for booking, activity in created:
        db.refresh(booking)
        refs.append(booking.booking_ref)
        if booking.customer_email:
            try:
                EmailService.send_booking_confirmation_email(
                    user_email=booking.customer_email,
                    user_name=booking.customer_name or "Guest",
                    booking_reference=booking.booking_ref,
                    activity_title=activity.title,
                    booking_date=booking.booking_date.strftime("%B %d, %Y"),
                    total_amount=f"€{booking.total_price:.2f}",
                )
            except Exception as e:
                logger.error(f"Failed to send booking confirmation email: {e}")

    # Clear the cart now that the order is placed.
    if cart_session_id:
        db.query(CartItem).filter(CartItem.session_id == cart_session_id).delete()
        db.commit()

    return {"status": "paid", "booking_refs": refs, "first_ref": refs[0] if refs else None}
