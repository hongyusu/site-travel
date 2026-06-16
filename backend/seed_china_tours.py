#!/usr/bin/env python3
"""Seed 8 China regional tours (from site-finuo) as bilingual activities.

Creates 2 new destinations (Anhui, Suzhou), reuses existing Shanghai & Hangzhou,
and adds 8 fully-detailed activities (English primary + Chinese translations) under
the existing "Dragon Gate Travel" vendor.

Prices: stored in EUR as (CNY / 10) so the site's flat 10x EUR->CNY conversion shows
the exact original yuan price to CN-location users.

Run inside the backend container:
    docker exec travel_backend python /app/seed_china_tours.py
Idempotent: skips destinations/activities whose slug already exists.
"""

import json
import os
import sys
from decimal import Decimal

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.user import Vendor
from app.models.activity import (
    Category, Destination, Activity, ActivityImage, ActivityCategory,
    ActivityDestination, ActivityHighlight, ActivityInclude, ActivityFAQ,
    MeetingPoint, ActivityTimeline,
)
from app.models.translation import (
    ActivityTranslation, ActivityHighlightTranslation, ActivityIncludeTranslation,
    ActivityFAQTranslation, ActivityTimelineTranslation, MeetingPointTranslation,
    DestinationTranslation,
)

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

DURATION_MIN = 3 * 24 * 60  # 3-day tours
GROUP = 30
LANGS = ["english", "chinese"]
VENDOR_COMPANY = "Dragon Gate Travel"

# ── New destinations (existing Shanghai/Hangzhou are reused, not recreated) ────
NEW_DESTINATIONS = [
    # name, slug, country, code, lat, lng, featured, zh_name
    ("Anhui", "anhui", "China", "CN", 31.8206, 117.2272, True, "安徽"),
    ("Suzhou", "suzhou", "China", "CN", 31.2989, 120.5853, True, "苏州"),
]
# zh names to ensure on any destination we link (incl. existing)
DEST_ZH = {"anhui": "安徽", "suzhou": "苏州", "shanghai": "上海", "hangzhou": "杭州"}

# ── Meeting points (by key) ────────────────────────────────────────────────────
MEET = {
    "anhui": (
        "Hefei departure point — hotel or Hefei South Railway Station pickup, Anhui, China",
        "合肥出发集合点 —— 酒店或合肥南站接站，中国安徽",
    ),
    "suzhou": (
        "Suzhou — airport or high-speed railway station pickup, China",
        "苏州 —— 机场或高铁站接站，中国",
    ),
    "hangzhou": (
        "Hangzhou — airport pickup, China",
        "杭州 —— 机场接站，中国",
    ),
    "shanghai": (
        "Shanghai — Pudong International Airport (PVG) pickup, China",
        "上海 —— 浦东国际机场接站，中国",
    ),
}

# ── Shared includes (item_en, item_zh, is_included) ────────────────────────────
INCLUDES = [
    ("Air-conditioned coach transport throughout the 3 days", "全程空调旅游巴士", True),
    ("2 nights in 4-star (or 4-diamond) hotels — twin room with breakfast",
     "2 晚四星 / 4 钻酒店（双标间含双早）", True),
    ("5 meals as listed in the itinerary", "行程所列 5 正餐", True),
    ("All attraction entrance tickets listed in the itinerary", "行程所列景点门票", True),
    ("Full-time English-speaking guide for all 3 days", "全程 3 天英语导游 1 名", True),
    ("Travel accident insurance (CNY 200,000 coverage per person)",
     "旅游人身意外险（20 万元 / 人）", True),
    ("2 bottles of water per person per day", "每人每天 2 瓶矿泉水", True),
    ("International and domestic flights", "国际及国内段机票", False),
    ("Personal expenses and souvenirs", "个人消费与纪念品", False),
    ("Gratuities (optional)", "小费（自愿）", False),
    ("Optional activities not listed in the itinerary", "行程外自选项目", False),
]

# ── Shared FAQs (q_en, a_en, q_zh, a_zh) ───────────────────────────────────────
FAQS = [
    (
        "Do I need a visa to join this tour?",
        "Finnish and most European passport holders currently enjoy 30-day visa-free entry "
        "to China (policy valid through the end of 2026). Travellers of other nationalities "
        "can often use the 240-hour visa-free transit or apply for an L tourist visa. Bring "
        "your hotel address and onward ticket for the entry card.",
        "参加此行程需要签证吗？",
        "芬兰及大多数欧洲国家护照目前可免签入境中国停留 30 天（政策有效期至 2026 年底）。"
        "其他国家旅客通常可使用 240 小时过境免签，或申请 L 类旅游签证。入境时请备好酒店地址与续程机票信息。",
    ),
    (
        "What is included in the price?",
        "The price covers air-conditioned coach transport, 2 nights in 4-star hotels with "
        "breakfast, 5 meals, all listed entrance tickets, a full-time English-speaking guide, "
        "and travel accident insurance. International and domestic flights, personal expenses "
        "and gratuities are not included.",
        "费用包含哪些内容？",
        "费用包含全程空调旅游巴士、2 晚四星酒店（含早）、5 正餐、行程所列景点门票、全程英语导游"
        "以及旅游人身意外险。国际及国内段机票、个人消费与小费不含在内。",
    ),
    (
        "How do I pay for personal expenses in China?",
        "China is largely cashless — Alipay and WeChat Pay are accepted almost everywhere and "
        "both now support foreign Visa and Mastercard. We recommend carrying CNY 200–500 in "
        "cash as a backup. There is no tipping culture in China.",
        "在中国如何支付个人消费？",
        "中国基本无现金 —— 支付宝和微信支付几乎覆盖所有场所，且均支持境外 Visa 与 Mastercard。"
        "建议随身携带 200–500 元现金以备不时之需。中国没有小费文化。",
    ),
    (
        "Can this tour be booked privately or for a single traveller?",
        "Yes. The itinerary can be booked individually or as a private group, and we are happy "
        "to customize the days and city combination on request.",
        "可以单人预订或包团吗？",
        "可以。行程支持单人预订或包团出行，并可根据需求定制天数与城市组合。",
    ),
]

# ── Per-tour metadata keyed by slug ────────────────────────────────────────────
TOUR_META = {
    "china-huangshan-yellow-mountain-3-day": dict(
        price_cny=1727, dests=["anhui"], cats=["tours", "nature", "outdoor"],
        meet="anhui", bestseller=True, weather=True, rating="4.9", reviews=86, bookings=240),
    "china-huizhou-ancient-villages-3-day": dict(
        price_cny=1535, dests=["anhui"], cats=["tours", "historical", "nature"],
        meet="anhui", bestseller=False, weather=False, rating="4.8", reviews=54, bookings=160),
    "china-mount-qiyun-3-day": dict(
        price_cny=1629, dests=["anhui"], cats=["tours", "nature", "historical"],
        meet="anhui", bestseller=False, weather=True, rating="4.7", reviews=38, bookings=120),
    "china-southern-anhui-jingxian-3-day": dict(
        price_cny=1491, dests=["anhui"], cats=["tours", "nature", "art-workshops"],
        meet="anhui", bestseller=False, weather=True, rating="4.7", reviews=33, bookings=95),
    "china-suzhou-classical-gardens-3-day": dict(
        price_cny=1756, dests=["suzhou"], cats=["tours", "historical", "museums"],
        meet="suzhou", bestseller=True, weather=False, rating="4.9", reviews=72, bookings=210),
    "china-hangzhou-west-lake-3-day": dict(
        price_cny=1805, dests=["hangzhou"], cats=["tours", "nature", "historical"],
        meet="hangzhou", bestseller=False, weather=False, rating="4.8", reviews=65, bookings=190),
    "china-suzhou-hangzhou-3-day": dict(
        price_cny=1846, dests=["suzhou", "hangzhou"], cats=["tours", "historical", "nature"],
        meet="suzhou", bestseller=True, weather=False, rating="4.8", reviews=58, bookings=175),
    "china-shanghai-city-3-day": dict(
        price_cny=1842, dests=["shanghai"], cats=["tours", "historical", "museums"],
        meet="shanghai", bestseller=True, weather=False, rating="4.9", reviews=91, bookings=260),
}

# ── Bilingual content (filled from the content workflow) ───────────────────────
# Each item: slug, title_en, title_zh, short_en, short_zh, desc_en, desc_zh,
#            what_to_bring_en, what_to_bring_zh,
#            highlights:[{en,zh}], timeline:[{day,title_en,title_zh,desc_en,desc_zh}]
_CONTENT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "china_tours_content.json")
with open(_CONTENT_PATH, encoding="utf-8") as _f:
    TOURS_CONTENT = json.load(_f)


def run():
    session = Session()
    try:
        # 0. Fix sequences (out of sync after backup restore)
        for table in (
            "destinations", "destination_translations", "activities",
            "activity_images", "activity_highlights", "activity_includes",
            "activity_faqs", "activity_timelines", "meeting_points",
            "activity_translations", "activity_highlight_translations",
            "activity_include_translations", "activity_faq_translations",
            "activity_timeline_translations", "meeting_point_translations",
        ):
            session.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                f"COALESCE((SELECT MAX(id) FROM {table}), 0) + 1, false)"
            ))
        session.commit()

        # 1. Destinations
        dest_map = {d.slug: d for d in session.query(Destination).all()}
        for name, slug, country, code, lat, lng, feat, _zh in NEW_DESTINATIONS:
            if slug not in dest_map:
                d = Destination(
                    name=name, slug=slug, country=country, country_code=code,
                    image_url=f"https://picsum.photos/seed/{slug}-dest/800/600",
                    latitude=lat, longitude=lng, is_featured=feat,
                )
                session.add(d)
                session.flush()
                dest_map[slug] = d
                print(f"  + Destination: {name}")
            else:
                print(f"  = Destination exists: {name}")

        # zh translations for linked destinations (skip if present)
        for slug, zh in DEST_ZH.items():
            d = dest_map.get(slug)
            if not d:
                continue
            exists = session.query(DestinationTranslation).filter_by(
                destination_id=d.id, language="zh").first()
            if not exists:
                session.add(DestinationTranslation(
                    destination_id=d.id, language="zh", name=zh))
                print(f"  + Destination zh: {slug} -> {zh}")

        # 2. Vendor
        vendor = session.query(Vendor).filter_by(company_name=VENDOR_COMPANY).first()
        if not vendor:
            vendor = session.query(Vendor).first()
        vid = vendor.id
        print(f"  Vendor: {vendor.company_name} (id={vid})")

        cat_map = {c.slug: c for c in session.query(Category).all()}

        # 3. Activities
        added = 0
        for c in TOURS_CONTENT:
            slug = c["slug"]
            meta = TOUR_META[slug]
            if session.query(Activity).filter_by(slug=slug).first():
                print(f"  = Activity exists: {slug}")
                continue

            price = (Decimal(str(meta["price_cny"])) / 10).quantize(Decimal("0.01"))
            child = (price * Decimal("0.7")).quantize(Decimal("0.01"))

            act = Activity(
                vendor_id=vid,
                title=c["title_en"], slug=slug,
                description=c["desc_en"], short_description=c["short_en"],
                price_adult=price, price_child=child, price_currency="EUR",
                duration_minutes=DURATION_MIN, max_group_size=GROUP,
                instant_confirmation=False, free_cancellation_hours=72,
                languages=LANGS, is_bestseller=meta["bestseller"], is_skip_the_line=False,
                is_active=True, has_multiple_tiers=False,
                is_likely_to_sell_out=meta["bestseller"], has_mobile_ticket=True,
                has_best_price_guarantee=True, is_verified_activity=True,
                response_time_hours=24, allows_service_animals=True,
                weather_dependent=meta["weather"], what_to_bring=c["what_to_bring_en"],
                has_covid_measures=False, is_giftable=True,
                allows_reserve_now_pay_later=True, reserve_payment_deadline_hours=72,
                average_rating=Decimal(meta["rating"]),
                total_reviews=meta["reviews"], total_bookings=meta["bookings"],
            )
            session.add(act)
            session.flush()
            aid = act.id

            # activity zh translation
            session.add(ActivityTranslation(
                activity_id=aid, language="zh",
                title=c["title_zh"], short_description=c["short_zh"],
                description=c["desc_zh"], what_to_bring=c["what_to_bring_zh"],
            ))

            # images
            for i in range(6):
                session.add(ActivityImage(
                    activity_id=aid,
                    url=f"https://picsum.photos/seed/{slug}-image-{i}/800/600",
                    alt_text=f"{c['title_en']} - Image {i + 1}",
                    is_primary=(i == 0), is_hero=(i == 0), order_index=i,
                ))

            # categories
            for cs in meta["cats"]:
                if cs in cat_map:
                    session.add(ActivityCategory(activity_id=aid, category_id=cat_map[cs].id))

            # destinations
            for ds in meta["dests"]:
                if ds in dest_map:
                    session.add(ActivityDestination(
                        activity_id=aid, destination_id=dest_map[ds].id))

            # highlights (+ zh)
            for i, h in enumerate(c["highlights"]):
                hl = ActivityHighlight(activity_id=aid, text=h["en"], order_index=i)
                session.add(hl)
                session.flush()
                session.add(ActivityHighlightTranslation(
                    highlight_id=hl.id, language="zh", text=h["zh"]))

            # includes (+ zh)
            for i, (en, zh, inc) in enumerate(INCLUDES):
                it = ActivityInclude(activity_id=aid, item=en, is_included=inc, order_index=i)
                session.add(it)
                session.flush()
                session.add(ActivityIncludeTranslation(
                    include_id=it.id, language="zh", item=zh))

            # faqs (+ zh)
            for i, (qen, aen, qzh, azh) in enumerate(FAQS):
                f = ActivityFAQ(activity_id=aid, question=qen, answer=aen, order_index=i)
                session.add(f)
                session.flush()
                session.add(ActivityFAQTranslation(
                    faq_id=f.id, language="zh", question=qzh, answer=azh))

            # timeline (+ zh) — one step per day
            for step in c["timeline"]:
                tl = ActivityTimeline(
                    activity_id=aid, step_number=step["day"],
                    title=step["title_en"], description=step["desc_en"],
                    image_url=f"https://picsum.photos/seed/{slug}-day-{step['day']}/600/400",
                    order_index=step["day"] - 1,
                )
                session.add(tl)
                session.flush()
                session.add(ActivityTimelineTranslation(
                    timeline_id=tl.id, language="zh",
                    title=step["title_zh"], description=step["desc_zh"]))

            # meeting point (+ zh)
            men, mzh = MEET[meta["meet"]]
            dobj = dest_map.get(meta["dests"][0])
            mp = MeetingPoint(
                activity_id=aid, address=men,
                instructions="Your guide will confirm the exact pickup time and point after booking.",
                latitude=dobj.latitude if dobj else None,
                longitude=dobj.longitude if dobj else None,
                public_transport_info="Hotel / airport / railway station pickup included.",
            )
            session.add(mp)
            session.flush()
            session.add(MeetingPointTranslation(
                meeting_point_id=mp.id, language="zh", address=mzh,
                instructions="预订后导游将与您确认具体接站时间与地点。",
                public_transport_info="含酒店 / 机场 / 高铁站接站。"))

            added += 1
            print(f"  + Activity: {c['title_en']}  (€{price} / ¥{meta['price_cny']})")

        session.commit()
        print(f"\nDone. Added {added} activities.")
        print("Totals:",
              "destinations=", session.query(Destination).count(),
              "activities=", session.query(Activity).count())
    except Exception as e:
        session.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
