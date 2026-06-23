#!/usr/bin/env python3
"""Seed Chinese (zh) translations for pricing tiers and add-ons (idempotent).

These two entity types were the only translatable activity content lacking zh
rows (titles, descriptions, highlights, includes, faqs, timelines, meeting
points, categories and destinations already have 100% zh coverage; English is
the primary columns). Both are heavily templated, so a small fixed set of
distinct strings (3 tier names + 8 tier descriptions, 7 add-on names + 7
add-on descriptions) is applied by exact English match across every row.

Run inside the backend container:
    docker exec travel_backend python /app/seed_zh_tiers_addons.py
Idempotent: skips any tier/add-on that already has a zh translation row.
"""

import os
import sys

from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate"
)
engine = create_engine(DATABASE_URL)

TIER_NAME_ZH = {
    "Standard": "标准",
    "Premium": "高级",
    "VIP": "贵宾",
}
TIER_DESC_ZH = {
    "Basic experience with all core activities": "基础体验，包含全部核心活动",
    "Enhanced experience with priority access and extras": "升级体验，享优先入场及额外服务",
    "Luxury experience with exclusive access and perks": "奢华体验，享专属通道及尊享礼遇",
    "Enhanced experience with additional perks": "升级体验，享额外礼遇",
    "Luxury experience with exclusive access": "奢华体验，享专属通道",
    "Enhanced experience with additional perks and smaller groups": "升级体验，享额外礼遇及小团出行",
    "Luxury experience with private guide and exclusive access": "奢华体验，配私人向导及专属通道",
    "Basic tour experience with professional guide": "基础游览体验，配专业向导",
}
ADDON_NAME_ZH = {
    "Extended Experience": "延长体验",
    "Private Upgrade": "私享升级",
    "Professional Photography": "专业摄影",
    "Professional Photography Package": "专业摄影套餐",
    "Souvenir Package": "纪念品套餐",
    "Traditional Lunch": "传统午餐",
    "Transportation Upgrade": "交通升级",
}
ADDON_DESC_ZH = {
    "Add extra time with additional stops or activities": "增加额外时间，包含更多景点或活动",
    "Upgrade to a private experience for your group only": "升级为仅限您团队的私人体验",
    "Professional photographer to capture your experience": "专业摄影师记录您的精彩体验",
    "Professional photos of your experience delivered digitally within 24 hours":
        "专业摄影作品，24小时内以电子版交付",
    "Curated selection of local souvenirs and gifts": "精选当地纪念品与礼品",
    "Authentic local cuisine lunch experience": "正宗当地美食午餐体验",
    "Private vehicle instead of group transportation": "以私人车辆替代团体交通",
}


def _zh(mapping: dict, value: str | None) -> str | None:
    """Return the zh string for an English value, falling back to the original."""
    if value is None or value == "":
        return None
    return mapping.get(value, value)


def main() -> None:
    """Insert zh translation rows for pricing tiers + add-ons that lack them."""
    with engine.begin() as conn:
        ins_t = 0
        for t in conn.execute(
            text("SELECT id, tier_name, tier_description FROM activity_pricing_tiers")
        ).fetchall():
            if conn.execute(
                text("SELECT 1 FROM activity_pricing_tier_translations "
                     "WHERE pricing_tier_id=:id AND language='zh'"),
                {"id": t.id},
            ).first():
                continue
            conn.execute(
                text("INSERT INTO activity_pricing_tier_translations "
                     "(pricing_tier_id, language, tier_name, tier_description) "
                     "VALUES (:id, 'zh', :n, :d)"),
                {"id": t.id, "n": _zh(TIER_NAME_ZH, t.tier_name),
                 "d": _zh(TIER_DESC_ZH, t.tier_description)},
            )
            ins_t += 1

        ins_a = 0
        for a in conn.execute(
            text("SELECT id, name, description FROM activity_add_ons")
        ).fetchall():
            if conn.execute(
                text("SELECT 1 FROM activity_addon_translations "
                     "WHERE addon_id=:id AND language='zh'"),
                {"id": a.id},
            ).first():
                continue
            conn.execute(
                text("INSERT INTO activity_addon_translations "
                     "(addon_id, language, name, description) "
                     "VALUES (:id, 'zh', :n, :d)"),
                {"id": a.id, "n": _zh(ADDON_NAME_ZH, a.name),
                 "d": _zh(ADDON_DESC_ZH, a.description)},
            )
            ins_a += 1

        print(f"Inserted zh translations: {ins_t} pricing tiers, {ins_a} add-ons.")

    # Verification summary (read-only).
    with engine.connect() as conn:
        for entity, base_tbl, tr_tbl, fk in [
            ("pricing_tiers", "activity_pricing_tiers",
             "activity_pricing_tier_translations", "pricing_tier_id"),
            ("add_ons", "activity_add_ons", "activity_addon_translations", "addon_id"),
        ]:
            base = conn.execute(text(f"SELECT count(*) FROM {base_tbl}")).scalar()
            zh = conn.execute(
                text(f"SELECT count(*) FROM {tr_tbl} WHERE language='zh'")
            ).scalar()
            print(f"  {entity:<14} zh coverage: {zh}/{base}")


if __name__ == "__main__":
    main()
