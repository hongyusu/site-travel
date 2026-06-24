#!/usr/bin/env python3
"""Re-sync editable content for Finuo-Giraffe activities from girafe_tours.json.

Updates short_description/description (+ zh) and rebuilds highlights, includes/
excludes and timeline (+ zh) IN PLACE for each existing Finuo-Giraffe activity
(matched by slug). Does NOT touch the activity row, images, pricing tiers,
meeting point, reviews or bookings — so seeded reviews/images are preserved.
Idempotent. Use after correcting girafe_tours.json.

    docker exec travel_backend python /app/resync_girafe_content.py
"""
import json, os, sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.models.activity import (
    Activity, ActivityHighlight, ActivityInclude, ActivityTimeline)
from app.models.translation import (
    ActivityTranslation, ActivityHighlightTranslation,
    ActivityIncludeTranslation, ActivityTimelineTranslation)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    tours = json.load(open(os.path.join(here, "girafe_tours.json"), encoding="utf-8"))
    s = Session()
    try:
        updated = 0
        for t in tours:
            act = s.query(Activity).filter_by(slug=t["slug"]).first()
            if not act:
                print(f"  ? not found: {t['slug']}"); continue
            aid = act.id
            # short_description / description (en + zh)
            act.short_description = t["short_en"]
            act.description = t["desc_en"]
            tr = s.query(ActivityTranslation).filter_by(activity_id=aid, language="zh").first()
            if tr:
                tr.short_description = t["short_zh"]; tr.description = t["desc_zh"]

            # highlights: delete (+ zh) then reinsert
            hids = [h.id for h in s.query(ActivityHighlight).filter_by(activity_id=aid).all()]
            if hids:
                s.query(ActivityHighlightTranslation).filter(
                    ActivityHighlightTranslation.highlight_id.in_(hids)).delete(synchronize_session=False)
                s.query(ActivityHighlight).filter_by(activity_id=aid).delete(synchronize_session=False)
            for i, h in enumerate(t["highlights"]):
                hl = ActivityHighlight(activity_id=aid, text=h["en"], order_index=i)
                s.add(hl); s.flush()
                s.add(ActivityHighlightTranslation(highlight_id=hl.id, language="zh", text=h["zh"]))

            # includes (+ excludes): delete (+ zh) then reinsert
            iids = [i.id for i in s.query(ActivityInclude).filter_by(activity_id=aid).all()]
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

            # timeline: delete (+ zh) then reinsert (keeps per-day image_url from json)
            tids = [tl.id for tl in s.query(ActivityTimeline).filter_by(activity_id=aid).all()]
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
            updated += 1
        s.commit()
        print(f"Re-synced content for {updated} Finuo-Giraffe activities.")
    except Exception as e:
        s.rollback(); print(f"ERROR: {e}"); raise
    finally:
        s.close()


if __name__ == "__main__":
    run()
