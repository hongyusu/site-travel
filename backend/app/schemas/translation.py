"""Translation schemas for API endpoints."""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class TranslationBase(BaseModel):
    """Base translation schema."""
    language: str = Field(..., regex="^(en|es|zh|fr)$", description="Language code")


class ActivityTranslationBase(TranslationBase):
    """Base schema for activity translations."""
    title: Optional[str] = Field(None, max_length=500)
    short_description: Optional[str] = None
    description: Optional[str] = None
    dress_code: Optional[str] = None
    what_to_bring: Optional[str] = None
    not_suitable_for: Optional[str] = None
    covid_measures: Optional[str] = None
    cancellation_policy: Optional[str] = None


class ActivityTranslationCreate(ActivityTranslationBase):
    """Schema for creating activity translations."""
    pass


class ActivityTranslationUpdate(ActivityTranslationBase):
    """Schema for updating activity translations."""
    language: Optional[str] = Field(None, regex="^(en|es|zh|fr)$")


class ActivityTranslationResponse(ActivityTranslationBase):
    """Schema for activity translation responses."""
    id: int
    activity_id: int

    class Config:
        from_attributes = True


class ActivityHighlightTranslationBase(TranslationBase):
    """Base schema for activity highlight translations."""
    text: Optional[str] = Field(None, max_length=500)


class ActivityHighlightTranslationCreate(ActivityHighlightTranslationBase):
    """Schema for creating activity highlight translations."""
    pass


class ActivityHighlightTranslationResponse(ActivityHighlightTranslationBase):
    """Schema for activity highlight translation responses."""
    id: int
    highlight_id: int

    class Config:
        from_attributes = True


class ActivityIncludeTranslationBase(TranslationBase):
    """Base schema for activity include translations."""
    item: Optional[str] = Field(None, max_length=500)


class ActivityIncludeTranslationCreate(ActivityIncludeTranslationBase):
    """Schema for creating activity include translations."""
    pass


class ActivityIncludeTranslationResponse(ActivityIncludeTranslationBase):
    """Schema for activity include translation responses."""
    id: int
    include_id: int

    class Config:
        from_attributes = True


class ActivityFAQTranslationBase(TranslationBase):
    """Base schema for activity FAQ translations."""
    question: Optional[str] = None
    answer: Optional[str] = None


class ActivityFAQTranslationCreate(ActivityFAQTranslationBase):
    """Schema for creating activity FAQ translations."""
    pass


class ActivityFAQTranslationResponse(ActivityFAQTranslationBase):
    """Schema for activity FAQ translation responses."""
    id: int
    faq_id: int

    class Config:
        from_attributes = True


class ActivityTimelineTranslationBase(TranslationBase):
    """Base schema for activity timeline translations."""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None


class ActivityTimelineTranslationCreate(ActivityTimelineTranslationBase):
    """Schema for creating activity timeline translations."""
    pass


class ActivityTimelineTranslationResponse(ActivityTimelineTranslationBase):
    """Schema for activity timeline translation responses."""
    id: int
    timeline_id: int

    class Config:
        from_attributes = True


class ActivityPricingTierTranslationBase(TranslationBase):
    """Base schema for activity pricing tier translations."""
    tier_name: Optional[str] = Field(None, max_length=100)
    tier_description: Optional[str] = None


class ActivityPricingTierTranslationCreate(ActivityPricingTierTranslationBase):
    """Schema for creating activity pricing tier translations."""
    pass


class ActivityPricingTierTranslationResponse(ActivityPricingTierTranslationBase):
    """Schema for activity pricing tier translation responses."""
    id: int
    pricing_tier_id: int

    class Config:
        from_attributes = True


class ActivityAddOnTranslationBase(TranslationBase):
    """Base schema for activity add-on translations."""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None


class ActivityAddOnTranslationCreate(ActivityAddOnTranslationBase):
    """Schema for creating activity add-on translations."""
    pass


class ActivityAddOnTranslationResponse(ActivityAddOnTranslationBase):
    """Schema for activity add-on translation responses."""
    id: int
    addon_id: int

    class Config:
        from_attributes = True


class MeetingPointTranslationBase(TranslationBase):
    """Base schema for meeting point translations."""
    address: Optional[str] = None
    instructions: Optional[str] = None
    parking_info: Optional[str] = None
    public_transport_info: Optional[str] = None
    nearby_landmarks: Optional[str] = None


class MeetingPointTranslationCreate(MeetingPointTranslationBase):
    """Schema for creating meeting point translations."""
    pass


class MeetingPointTranslationResponse(MeetingPointTranslationBase):
    """Schema for meeting point translation responses."""
    id: int
    meeting_point_id: int

    class Config:
        from_attributes = True


# Aggregated translation schemas for entire activities
class ActivityFullTranslation(BaseModel):
    """Full translation data for an activity."""
    language: str
    activity: Optional[ActivityTranslationResponse] = None
    highlights: List[ActivityHighlightTranslationResponse] = []
    includes: List[ActivityIncludeTranslationResponse] = []
    faqs: List[ActivityFAQTranslationResponse] = []
    timelines: List[ActivityTimelineTranslationResponse] = []
    pricing_tiers: List[ActivityPricingTierTranslationResponse] = []
    add_ons: List[ActivityAddOnTranslationResponse] = []
    meeting_point: Optional[MeetingPointTranslationResponse] = None


class ActivityTranslationsUpdate(BaseModel):
    """Schema for updating all translations for an activity."""
    translations: Dict[str, ActivityFullTranslation]