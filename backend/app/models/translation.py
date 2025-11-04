"""Translation models for multi-language support."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ActivityTranslation(Base):
    """Activity translation model."""

    __tablename__ = "activity_translations"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)  # 'en', 'es', 'zh', 'fr'
    title = Column(String(500))
    short_description = Column(Text)
    description = Column(Text)
    dress_code = Column(Text)
    what_to_bring = Column(Text)
    not_suitable_for = Column(Text)
    covid_measures = Column(Text)
    cancellation_policy = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    activity = relationship("Activity", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("activity_id", "language", name="uq_activity_language"),
    )


class ActivityHighlightTranslation(Base):
    """Activity highlight translation model."""

    __tablename__ = "activity_highlight_translations"

    id = Column(Integer, primary_key=True, index=True)
    highlight_id = Column(Integer, ForeignKey("activity_highlights.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)
    text = Column(String(500))

    # Relationships
    highlight = relationship("ActivityHighlight", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("highlight_id", "language", name="uq_highlight_language"),
    )


class ActivityIncludeTranslation(Base):
    """Activity include/exclude translation model."""

    __tablename__ = "activity_include_translations"

    id = Column(Integer, primary_key=True, index=True)
    include_id = Column(Integer, ForeignKey("activity_includes.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)
    item = Column(String(500))

    # Relationships
    include_item = relationship("ActivityInclude", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("include_id", "language", name="uq_include_language"),
    )


class ActivityFAQTranslation(Base):
    """Activity FAQ translation model."""

    __tablename__ = "activity_faq_translations"

    id = Column(Integer, primary_key=True, index=True)
    faq_id = Column(Integer, ForeignKey("activity_faqs.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)
    question = Column(Text)
    answer = Column(Text)

    # Relationships
    faq = relationship("ActivityFAQ", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("faq_id", "language", name="uq_faq_language"),
    )


class ActivityTimelineTranslation(Base):
    """Activity timeline translation model."""

    __tablename__ = "activity_timeline_translations"

    id = Column(Integer, primary_key=True, index=True)
    timeline_id = Column(Integer, ForeignKey("activity_timelines.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)
    title = Column(String(255))
    description = Column(Text)

    # Relationships
    timeline = relationship("ActivityTimeline", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("timeline_id", "language", name="uq_timeline_language"),
    )


class ActivityPricingTierTranslation(Base):
    """Activity pricing tier translation model."""

    __tablename__ = "activity_pricing_tier_translations"

    id = Column(Integer, primary_key=True, index=True)
    pricing_tier_id = Column(Integer, ForeignKey("activity_pricing_tiers.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)
    tier_name = Column(String(100))
    tier_description = Column(Text)

    # Relationships
    pricing_tier = relationship("ActivityPricingTier", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("pricing_tier_id", "language", name="uq_pricing_tier_language"),
    )


class ActivityAddOnTranslation(Base):
    """Activity add-on translation model."""

    __tablename__ = "activity_addon_translations"

    id = Column(Integer, primary_key=True, index=True)
    addon_id = Column(Integer, ForeignKey("activity_add_ons.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)
    name = Column(String(255))
    description = Column(Text)

    # Relationships
    addon = relationship("ActivityAddOn", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("addon_id", "language", name="uq_addon_language"),
    )


class MeetingPointTranslation(Base):
    """Meeting point translation model."""

    __tablename__ = "meeting_point_translations"

    id = Column(Integer, primary_key=True, index=True)
    meeting_point_id = Column(Integer, ForeignKey("meeting_points.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)
    address = Column(Text)
    instructions = Column(Text)
    parking_info = Column(Text)
    public_transport_info = Column(Text)
    nearby_landmarks = Column(Text)

    # Relationships
    meeting_point = relationship("MeetingPoint", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("meeting_point_id", "language", name="uq_meeting_point_language"),
    )


class CategoryTranslation(Base):
    """Category translation model."""

    __tablename__ = "category_translations"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)  # 'en', 'es', 'zh', 'fr'
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("category_id", "language", name="uq_category_language"),
    )


class DestinationTranslation(Base):
    """Destination translation model."""

    __tablename__ = "destination_translations"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)  # 'en', 'es', 'zh', 'fr'
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    destination = relationship("Destination", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("destination_id", "language", name="uq_destination_language"),
    )