#!/usr/bin/env python3
"""Seed Girafe (Finuo-Giraffe) European group tours as bilingual activities.

Creates the "Finuo-Giraffe" provider (vendor + backing user), the European
region destinations, and one activity per tour from backend/girafe_tours.json
(built from the scraped paris-girafe.com catalog). Content is English (primary
columns) + Simplified Chinese (translation tables); prices are real EUR with
1-/2-/3-person pricing tiers. Tours are marked is_available=True (Finuo provider).

Run inside the backend container:
    docker exec travel_backend python /app/seed_girafe_tours.py
Idempotent: skips destinations / vendor / activities that already exist (by slug
/ company_name).
"""

import json
import os
import sys
from decimal import Decimal

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.user import User, UserRole, Vendor
from app.models.activity import (
    Category, Destination, Activity, ActivityImage, ActivityCategory,
    ActivityDestination, ActivityHighlight, ActivityInclude, ActivityFAQ,
    MeetingPoint, ActivityTimeline, ActivityPricingTier,
)
from app.models.translation import (
    ActivityTranslation, ActivityHighlightTranslation, ActivityIncludeTranslation,
    ActivityFAQTranslation, ActivityTimelineTranslation, MeetingPointTranslation,
    DestinationTranslation, ActivityPricingTierTranslation,
)

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

VENDOR_COMPANY = "Finuo-Giraffe"
VENDOR_EMAIL = "partner.giraffe@finuo.fi"
PW_HASH = "$2b$12$TxjAN.QLj4nory7k.VFcF.SSwEEM8e1bPYaVVf0vgMQ3QpI.YM0Cy"
LANGS = ["Chinese", "English"]
WEATHER_REGIONS = {"iceland-region", "norway-fjords", "switzerland-alps"}

WHAT_TO_BRING_EN = ("Valid passport and Schengen visa; comfortable walking shoes; "
                    "weather-appropriate clothing and a light rain jacket; a European "
                    "power adapter; and any personal medication.")
WHAT_TO_BRING_ZH = ("有效护照及申根签证；舒适的步行鞋；适合天气的衣物及轻便雨衣；"
                    "欧标电源转换插头；以及个人常备药品。")

FAQS = [
    ("Do I need a visa for this tour?",
     "Most travellers need a Schengen visa to enter Europe. We provide booking "
     "confirmations, hotel vouchers and an itinerary to support your application; "
     "the visa itself is arranged and paid for by the traveller.",
     "参加此行程需要签证吗？",
     "大多数旅客进入欧洲需办理申根签证。我们提供预订确认单、酒店凭证及行程单以协助您"
     "办理签证；签证本身由旅客自行申请并承担费用。"),
    ("What is included in the price?",
     "The price covers city-centre 4-star hotels with daily breakfast, all intercity "
     "transport, a licensed Chinese-speaking guide-driver, and all listed attraction "
     "entries and experiences — an all-inclusive price with no forced shopping. "
     "International flights, visa and insurance are not included.",
     "费用包含哪些内容？",
     "费用包含市中心四星级酒店及每日早餐、全程城际交通、持证中文司导，以及行程所列"
     "全部景点门票与体验项目——一价全含，无强制购物。国际机票、签证与保险不含在内。"),
    ("Is this a small-group or private tour?",
     "Group sizes vary by product (from intimate small groups to larger coach tours). "
     "Private departures and custom date/city combinations are available on request.",
     "这是小团还是私人团？",
     "团队规模因产品而异（从精致小团到大巴团均有）。亦可应需求安排私人发团及定制"
     "日期与城市组合。"),
    ("How do I pay and can I reserve now and pay later?",
     "You can reserve now and pay later before the payment deadline. Free cancellation "
     "is available up to 30 days before departure.",
     "如何付款？可以先预订后付款吗？",
     "支持先预订后付款，在付款截止日期前完成支付即可。出发前 30 天可免费取消。"),
]


def get_or_create_vendor(session):
    """Create (or fetch) the Finuo-Giraffe vendor and its backing user."""
    vendor = session.query(Vendor).filter_by(company_name=VENDOR_COMPANY).first()
    if vendor:
        print(f"  = Vendor exists: {VENDOR_COMPANY} (id={vendor.id})")
        return vendor
    user = session.query(User).filter_by(email=VENDOR_EMAIL).first()
    if not user:
        user = User(email=VENDOR_EMAIL, password_hash=PW_HASH,
                    full_name="Finuo-Giraffe", role=UserRole.VENDOR,
                    email_verified=True, is_active=True)
        session.add(user); session.flush()
    vendor = Vendor(user_id=user.id, company_name=VENDOR_COMPANY,
                    description=("Finuo's European specialist — premium guided multi-country "
                                 "tours across France, Italy, Switzerland, the Nordics and beyond."),
                    is_verified=True)
    session.add(vendor); session.flush()
    print(f"  + Vendor: {VENDOR_COMPANY} (id={vendor.id})")
    return vendor


def run():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "girafe_tours.json")
    tours = json.load(open(path, encoding="utf-8"))
    session = Session()
    try:
        for table in (
            "users", "vendors", "destinations", "destination_translations", "activities",
            "activity_images", "activity_highlights", "activity_includes", "activity_faqs",
            "activity_timelines", "meeting_points", "activity_pricing_tiers",
            "activity_translations", "activity_highlight_translations",
            "activity_include_translations", "activity_faq_translations",
            "activity_timeline_translations", "meeting_point_translations",
            "activity_pricing_tier_translations",
        ):
            session.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                f"COALESCE((SELECT MAX(id) FROM {table}), 0) + 1, false)"))
        session.commit()

        vendor = get_or_create_vendor(session)
        cat_map = {c.slug: c for c in session.query(Category).all()}
        dest_map = {d.slug: d for d in session.query(Destination).all()}

        # region destinations
        for t in tours:
            r = t["region"]
            if r["slug"] not in dest_map:
                d = Destination(name=r["name_en"], slug=r["slug"], country=r["country"],
                                country_code=r["code"], is_featured=True,
                                image_url=(t.get("primary_image") or None))
                session.add(d); session.flush(); dest_map[r["slug"]] = d
                session.add(DestinationTranslation(destination_id=d.id, language="zh", name=r["name_zh"]))
                print(f"  + Region destination: {r['name_en']} ({r['slug']})")

        added = 0
        for t in tours:
            slug = t["slug"]
            if session.query(Activity).filter_by(slug=slug).first():
                print(f"  = Activity exists: {slug}")
                continue
            weather = t["region"]["slug"] in WEATHER_REGIONS
            act = Activity(
                vendor_id=vendor.id, title=t["title_en"], slug=slug,
                description=t["desc_en"], short_description=t["short_en"],
                price_adult=Decimal(str(t["price_adult_eur"])), price_currency="EUR",
                duration_minutes=t["duration_days"] * 24 * 60, max_group_size=t["max_group_size"],
                instant_confirmation=False, free_cancellation_hours=720, languages=LANGS,
                is_bestseller=False, is_skip_the_line=False, is_active=True, is_available=True,
                has_multiple_tiers=bool(t.get("price_tiers")), has_mobile_ticket=True,
                has_best_price_guarantee=True, is_verified_activity=True, response_time_hours=24,
                weather_dependent=weather, what_to_bring=WHAT_TO_BRING_EN, has_covid_measures=False,
                is_giftable=True, allows_reserve_now_pay_later=True, reserve_payment_deadline_hours=720,
                average_rating=Decimal("0"), total_reviews=0, total_bookings=0,
            )
            session.add(act); session.flush(); aid = act.id
            session.add(ActivityTranslation(
                activity_id=aid, language="zh", title=t["title_zh"],
                short_description=t["short_zh"], description=t["desc_zh"],
                what_to_bring=WHAT_TO_BRING_ZH))

            # images
            gallery = t.get("gallery") or []
            for i, url in enumerate(gallery):
                session.add(ActivityImage(activity_id=aid, url=url,
                    alt_text=f"{t['title_en']} - {i + 1}", is_primary=(i == 0),
                    is_hero=(i == 0), order_index=i))

            # categories
            for cs in t["category_slugs"]:
                if cs in cat_map:
                    session.add(ActivityCategory(activity_id=aid, category_id=cat_map[cs].id))
            # destinations: region + matched gateway cities
            link = [t["region"]["slug"]] + [g for g in t.get("gateway_dest_slugs", [])]
            for ds in dict.fromkeys(link):
                if ds in dest_map:
                    session.add(ActivityDestination(activity_id=aid, destination_id=dest_map[ds].id))

            # highlights
            for i, h in enumerate(t["highlights"]):
                hl = ActivityHighlight(activity_id=aid, text=h["en"], order_index=i)
                session.add(hl); session.flush()
                session.add(ActivityHighlightTranslation(highlight_id=hl.id, language="zh", text=h["zh"]))
            # includes (is_included=True) + excludes (False)
            idx = 0
            for inc in t["includes"]:
                it = ActivityInclude(activity_id=aid, item=inc["en"], is_included=True, order_index=idx)
                session.add(it); session.flush()
                session.add(ActivityIncludeTranslation(include_id=it.id, language="zh", item=inc["zh"]))
                idx += 1
            for exc in t["excludes"]:
                it = ActivityInclude(activity_id=aid, item=exc["en"], is_included=False, order_index=idx)
                session.add(it); session.flush()
                session.add(ActivityIncludeTranslation(include_id=it.id, language="zh", item=exc["zh"]))
                idx += 1
            # faqs (shared)
            for i, (qen, aen, qzh, azh) in enumerate(FAQS):
                f = ActivityFAQ(activity_id=aid, question=qen, answer=aen, order_index=i)
                session.add(f); session.flush()
                session.add(ActivityFAQTranslation(faq_id=f.id, language="zh", question=qzh, answer=azh))
            # timeline
            for step in t["timeline"]:
                tl = ActivityTimeline(activity_id=aid, step_number=step["day"],
                    title=step["title_en"], description=step["description_en"],
                    image_url=step.get("image_url"), order_index=step["day"] - 1)
                session.add(tl); session.flush()
                session.add(ActivityTimelineTranslation(timeline_id=tl.id, language="zh",
                    title=step["title_zh"], description=step["description_zh"]))
            # pricing tiers
            for i, tier in enumerate(t.get("price_tiers", [])):
                pt = ActivityPricingTier(activity_id=aid, tier_name=tier["label_en"],
                    tier_description="", price_adult=Decimal(str(tier["price_eur"])),
                    order_index=i, is_active=True)
                session.add(pt); session.flush()
                session.add(ActivityPricingTierTranslation(pricing_tier_id=pt.id, language="zh",
                    tier_name=tier["label_zh"], tier_description=""))
            # meeting point
            mp = MeetingPoint(activity_id=aid, address=t["meeting_en"],
                instructions="Your guide will confirm the exact departure time and meeting point after booking.")
            session.add(mp); session.flush()
            session.add(MeetingPointTranslation(meeting_point_id=mp.id, language="zh",
                address=t["meeting_zh"], instructions="预订后导游将与您确认具体出发时间与集合地点。"))

            added += 1
            print(f"  + Activity: {t['title_en']}  (€{t['price_adult_eur']}, {t['duration_days']}d)")

        session.commit()
        print(f"\nDone. Added {added} activities under {VENDOR_COMPANY}.")
        print("Totals: destinations=", session.query(Destination).count(),
              "activities=", session.query(Activity).count())
    except Exception as e:
        session.rollback(); print(f"ERROR: {e}"); raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
