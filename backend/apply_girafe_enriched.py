#!/usr/bin/env python3
"""Apply comprehensive (enriched) content to Finuo-Giraffe activities IN PLACE.

For each tour in girafe_tours.json, rebuilds the timeline (comprehensive
day-by-day), includes/excludes (faithful to the operator's 費用包含/不包含),
FAQs (per-tour 常見問題 + visa + booking + safety), and image gallery — without
touching the activity row, pricing tiers, meeting point, reviews or bookings.
Idempotent. Run after seeding + after updating girafe_tours.json.

    docker exec travel_backend python /app/apply_girafe_enriched.py
"""
import json, os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.models.activity import (
    Activity, ActivityImage, ActivityInclude, ActivityFAQ, ActivityTimeline)
from app.models.translation import (
    ActivityIncludeTranslation, ActivityFAQTranslation, ActivityTimelineTranslation)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    tours = json.load(open(os.path.join(here, "girafe_tours.json"), encoding="utf-8"))
    s = Session()
    try:
        n = 0
        for t in tours:
            act = s.query(Activity).filter_by(slug=t["slug"]).first()
            if not act:
                print("  ? missing", t["slug"]); continue
            aid = act.id

            # includes / excludes (delete + reinsert)
            iids = [x.id for x in s.query(ActivityInclude).filter_by(activity_id=aid).all()]
            if iids:
                s.query(ActivityIncludeTranslation).filter(
                    ActivityIncludeTranslation.include_id.in_(iids)).delete(synchronize_session=False)
                s.query(ActivityInclude).filter_by(activity_id=aid).delete(synchronize_session=False)
            idx = 0
            for inc in t["includes"]:
                it = ActivityInclude(activity_id=aid, item=inc["en"], is_included=True, order_index=idx)
                s.add(it); s.flush()
                s.add(ActivityIncludeTranslation(include_id=it.id, language="zh", item=inc["zh"])); idx += 1
            for exc in t["excludes"]:
                it = ActivityInclude(activity_id=aid, item=exc["en"], is_included=False, order_index=idx)
                s.add(it); s.flush()
                s.add(ActivityIncludeTranslation(include_id=it.id, language="zh", item=exc["zh"])); idx += 1

            # faqs (delete + reinsert from per-tour faqs)
            fids = [x.id for x in s.query(ActivityFAQ).filter_by(activity_id=aid).all()]
            if fids:
                s.query(ActivityFAQTranslation).filter(
                    ActivityFAQTranslation.faq_id.in_(fids)).delete(synchronize_session=False)
                s.query(ActivityFAQ).filter_by(activity_id=aid).delete(synchronize_session=False)
            for i, f in enumerate(t.get("faqs", [])):
                fq = ActivityFAQ(activity_id=aid, question=f["question_en"], answer=f["answer_en"], order_index=i)
                s.add(fq); s.flush()
                s.add(ActivityFAQTranslation(faq_id=fq.id, language="zh",
                    question=f["question_zh"], answer=f["answer_zh"]))

            # timeline (delete + reinsert, comprehensive descriptions)
            tids = [x.id for x in s.query(ActivityTimeline).filter_by(activity_id=aid).all()]
            if tids:
                s.query(ActivityTimelineTranslation).filter(
                    ActivityTimelineTranslation.timeline_id.in_(tids)).delete(synchronize_session=False)
                s.query(ActivityTimeline).filter_by(activity_id=aid).delete(synchronize_session=False)
            for step in t["timeline"]:
                tl = ActivityTimeline(activity_id=aid, step_number=step["day"],
                    title=step["title_en"], description=step["description_en"],
                    image_url=step.get("image_url"), order_index=step["day"] - 1)
                s.add(tl); s.flush()
                s.add(ActivityTimelineTranslation(timeline_id=tl.id, language="zh",
                    title=step["title_zh"], description=step["description_zh"]))

            # images (delete + reinsert from gallery)
            gallery = t.get("gallery") or []
            if gallery:
                s.query(ActivityImage).filter_by(activity_id=aid).delete(synchronize_session=False)
                for i, url in enumerate(gallery):
                    s.add(ActivityImage(activity_id=aid, url=url, alt_text=f"{t['title_en']} - {i+1}",
                        is_primary=(i == 0), is_hero=(i == 0), order_index=i))
            n += 1
        s.commit()
        print(f"Applied enriched content to {n} Finuo-Giraffe activities.")
    except Exception as e:
        s.rollback(); print("ERROR:", e); raise
    finally:
        s.close()


if __name__ == "__main__":
    run()
