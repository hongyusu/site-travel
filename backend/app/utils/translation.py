"""Translation utility functions for multi-language support."""

from typing import Optional, Any, Dict, List
from sqlalchemy.orm import Session
from app.models import (
    Activity, ActivityTranslation,
    ActivityHighlight, ActivityHighlightTranslation,
    ActivityInclude, ActivityIncludeTranslation,
    ActivityFAQ, ActivityFAQTranslation,
    ActivityTimeline, ActivityTimelineTranslation,
    ActivityPricingTier, ActivityPricingTierTranslation,
    ActivityAddOn, ActivityAddOnTranslation,
    MeetingPoint, MeetingPointTranslation,
    Category, CategoryTranslation,
    Destination, DestinationTranslation
)


def get_translated_activity(activity: Activity, language: str, db: Session) -> Dict[str, Any]:
    """
    Get translated activity data.
    If translation doesn't exist for the language, falls back to English (original data).
    """
    if language == 'en':
        # English is the default, no translation needed
        return {
            'title': activity.title,
            'short_description': activity.short_description,
            'description': activity.description,
            'dress_code': activity.dress_code,
            'what_to_bring': activity.what_to_bring,
            'not_suitable_for': activity.not_suitable_for,
            'covid_measures': activity.covid_measures
        }

    # Fetch translation for the specified language
    translation = db.query(ActivityTranslation).filter(
        ActivityTranslation.activity_id == activity.id,
        ActivityTranslation.language == language
    ).first()

    if translation:
        return {
            'title': translation.title or activity.title,
            'short_description': translation.short_description or activity.short_description,
            'description': translation.description,  # Return None if no translation
            'dress_code': translation.dress_code,
            'what_to_bring': translation.what_to_bring,
            'not_suitable_for': translation.not_suitable_for,
            'covid_measures': translation.covid_measures
        }

    # No translation available - return None for all fields except title/short_description
    return {
        'title': activity.title,  # Always show title (fallback to English)
        'short_description': activity.short_description,  # Always show short description (fallback to English)
        'description': None,  # Show "not available" instead of English
        'dress_code': None,
        'what_to_bring': None,
        'not_suitable_for': None,
        'covid_measures': None
    }


def get_translated_highlights(highlights: List[ActivityHighlight], language: str, db: Session) -> List[Dict[str, Any]]:
    """Get translated highlights."""
    if language == 'en':
        return [{'id': h.id, 'text': h.text, 'order_index': h.order_index} for h in highlights]

    result = []
    for highlight in highlights:
        translation = db.query(ActivityHighlightTranslation).filter(
            ActivityHighlightTranslation.highlight_id == highlight.id,
            ActivityHighlightTranslation.language == language
        ).first()

        result.append({
            'id': highlight.id,
            'text': translation.text if translation else None,
            'order_index': highlight.order_index
        })

    # Filter out items with no translation
    return [h for h in result if h['text'] is not None]


def get_translated_includes(includes: List[ActivityInclude], language: str, db: Session) -> List[Dict[str, Any]]:
    """Get translated includes/excludes."""
    if language == 'en':
        return [{
            'id': i.id,
            'item': i.item,
            'is_included': i.is_included,
            'order_index': i.order_index
        } for i in includes]

    result = []
    for include in includes:
        translation = db.query(ActivityIncludeTranslation).filter(
            ActivityIncludeTranslation.include_id == include.id,
            ActivityIncludeTranslation.language == language
        ).first()

        if translation and translation.item:
            result.append({
                'id': include.id,
                'item': translation.item,
                'is_included': include.is_included,
                'order_index': include.order_index
            })

    return result


def get_translated_faqs(faqs: List[ActivityFAQ], language: str, db: Session) -> List[Dict[str, Any]]:
    """Get translated FAQs."""
    if language == 'en':
        return [{
            'id': f.id,
            'question': f.question,
            'answer': f.answer,
            'order_index': f.order_index
        } for f in faqs]

    result = []
    for faq in faqs:
        translation = db.query(ActivityFAQTranslation).filter(
            ActivityFAQTranslation.faq_id == faq.id,
            ActivityFAQTranslation.language == language
        ).first()

        if translation and translation.question and translation.answer:
            result.append({
                'id': faq.id,
                'question': translation.question,
                'answer': translation.answer,
                'order_index': faq.order_index
            })

    return result


def get_translated_timelines(timelines: List[ActivityTimeline], language: str, db: Session) -> List[Dict[str, Any]]:
    """Get translated timelines."""
    if language == 'en':
        return [{
            'id': t.id,
            'step_number': t.step_number,
            'title': t.title,
            'description': t.description,
            'duration_minutes': t.duration_minutes,
            'image_url': t.image_url,
            'order_index': t.order_index
        } for t in timelines]

    result = []
    for timeline in timelines:
        translation = db.query(ActivityTimelineTranslation).filter(
            ActivityTimelineTranslation.timeline_id == timeline.id,
            ActivityTimelineTranslation.language == language
        ).first()

        if translation and translation.title:
            result.append({
                'id': timeline.id,
                'step_number': timeline.step_number,
                'title': translation.title,
                'description': translation.description,
                'duration_minutes': timeline.duration_minutes,
                'image_url': timeline.image_url,
                'order_index': timeline.order_index
            })

    return result


def get_translated_pricing_tiers(tiers: List[ActivityPricingTier], language: str, db: Session) -> List[Dict[str, Any]]:
    """Get translated pricing tiers."""
    if language == 'en':
        return [{
            'id': t.id,
            'tier_name': t.tier_name,
            'tier_description': t.tier_description,
            'price_adult': float(t.price_adult),
            'price_child': float(t.price_child) if t.price_child else None,
            'order_index': t.order_index,
            'is_active': t.is_active
        } for t in tiers]

    result = []
    for tier in tiers:
        translation = db.query(ActivityPricingTierTranslation).filter(
            ActivityPricingTierTranslation.pricing_tier_id == tier.id,
            ActivityPricingTierTranslation.language == language
        ).first()

        result.append({
            'id': tier.id,
            'tier_name': translation.tier_name if translation and translation.tier_name else tier.tier_name,
            'tier_description': translation.tier_description if translation and translation.tier_description else tier.tier_description,
            'price_adult': float(tier.price_adult),
            'price_child': float(tier.price_child) if tier.price_child else None,
            'order_index': tier.order_index,
            'is_active': tier.is_active
        })

    # Keep pricing tiers even without translation (price info is important)
    return result


def get_translated_add_ons(add_ons: List[ActivityAddOn], language: str, db: Session) -> List[Dict[str, Any]]:
    """Get translated add-ons."""
    if language == 'en':
        return [{
            'id': a.id,
            'name': a.name,
            'description': a.description,
            'price': float(a.price),
            'is_optional': a.is_optional,
            'order_index': a.order_index
        } for a in add_ons]

    result = []
    for addon in add_ons:
        translation = db.query(ActivityAddOnTranslation).filter(
            ActivityAddOnTranslation.addon_id == addon.id,
            ActivityAddOnTranslation.language == language
        ).first()

        result.append({
            'id': addon.id,
            'name': translation.name if translation and translation.name else addon.name,
            'description': translation.description if translation and translation.description else addon.description,
            'price': float(addon.price),
            'is_optional': addon.is_optional,
            'order_index': addon.order_index
        })

    # Keep add-ons even without translation (price info is important)
    return result


def get_translated_meeting_point(meeting_point: Optional[MeetingPoint], language: str, db: Session) -> Optional[Dict[str, Any]]:
    """Get translated meeting point."""
    if not meeting_point:
        return None

    if language == 'en':
        return {
            'id': meeting_point.id,
            'address': meeting_point.address,
            'instructions': meeting_point.instructions,
            'latitude': meeting_point.latitude,
            'longitude': meeting_point.longitude,
            'parking_info': meeting_point.parking_info,
            'public_transport_info': meeting_point.public_transport_info,
            'nearby_landmarks': meeting_point.nearby_landmarks,
            'photos': meeting_point.photos if hasattr(meeting_point, 'photos') else []
        }

    translation = db.query(MeetingPointTranslation).filter(
        MeetingPointTranslation.meeting_point_id == meeting_point.id,
        MeetingPointTranslation.language == language
    ).first()

    return {
        'id': meeting_point.id,
        'address': translation.address if translation and translation.address else meeting_point.address,
        'instructions': translation.instructions if translation and translation.instructions else meeting_point.instructions,
        'latitude': meeting_point.latitude,
        'longitude': meeting_point.longitude,
        'parking_info': translation.parking_info if translation and translation.parking_info else meeting_point.parking_info,
        'public_transport_info': translation.public_transport_info if translation and translation.public_transport_info else meeting_point.public_transport_info,
        'nearby_landmarks': translation.nearby_landmarks if translation and translation.nearby_landmarks else meeting_point.nearby_landmarks,
        'photos': meeting_point.photos if hasattr(meeting_point, 'photos') else []
    }


def validate_language(language: str) -> str:
    """Validate and normalize language code."""
    valid_languages = ['en', 'es', 'zh', 'fr']
    if language not in valid_languages:
        return 'en'  # Default to English
    return language


def get_translated_category(category: Category, language: str, db: Session) -> Dict[str, Any]:
    """Get translated category data."""
    if language == 'en':
        return {
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'icon': category.icon,
            'parent_id': category.parent_id,
            'order_index': category.order_index
        }

    translation = db.query(CategoryTranslation).filter(
        CategoryTranslation.category_id == category.id,
        CategoryTranslation.language == language
    ).first()

    return {
        'id': category.id,
        'name': translation.name if translation and translation.name else category.name,
        'slug': category.slug,
        'icon': category.icon,
        'parent_id': category.parent_id,
        'order_index': category.order_index
    }


def get_translated_destination(destination: Destination, language: str, db: Session) -> Dict[str, Any]:
    """Get translated destination data."""
    if language == 'en':
        return {
            'id': destination.id,
            'name': destination.name,
            'slug': destination.slug,
            'country': destination.country,
            'country_code': destination.country_code,
            'image_url': destination.image_url,
            'latitude': destination.latitude,
            'longitude': destination.longitude,
            'is_featured': destination.is_featured,
            'created_at': destination.created_at
        }

    translation = db.query(DestinationTranslation).filter(
        DestinationTranslation.destination_id == destination.id,
        DestinationTranslation.language == language
    ).first()

    return {
        'id': destination.id,
        'name': translation.name if translation and translation.name else destination.name,
        'slug': destination.slug,
        'country': destination.country,
        'country_code': destination.country_code,
        'image_url': destination.image_url,
        'latitude': destination.latitude,
        'longitude': destination.longitude,
        'is_featured': destination.is_featured,
        'created_at': destination.created_at
    }