#!/usr/bin/env python3
"""Re-sync ONLY the FAQs for Finuo-Giraffe activities from girafe_tours.json.

Replaces each activity's FAQs (+ zh translations) in place by slug. Touches
nothing else (images, timeline, sections, includes, reviews all untouched).
Idempotent.

    docker exec travel_backend python /app/apply_girafe_faqs.py
"""
import json, os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.models.activity import Activity, ActivityFAQ
from app.models.translation import ActivityFAQTranslation

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
            faqs = t.get("faqs")
            if not faqs:
                continue
            act = s.query(Activity).filter_by(slug=t["slug"]).first()
            if not act:
                continue
            fids = [x.id for x in s.query(ActivityFAQ).filter_by(activity_id=act.id).all()]
            if fids:
                s.query(ActivityFAQTranslation).filter(
                    ActivityFAQTranslation.faq_id.in_(fids)).delete(synchronize_session=False)
                s.query(ActivityFAQ).filter_by(activity_id=act.id).delete(synchronize_session=False)
            for i, f in enumerate(faqs):
                fq = ActivityFAQ(activity_id=act.id, question=f["question_en"], answer=f["answer_en"], order_index=i)
                s.add(fq); s.flush()
                s.add(ActivityFAQTranslation(faq_id=fq.id, language="zh",
                    question=f.get("question_zh") or f["question_en"],
                    answer=f.get("answer_zh") or f["answer_en"]))
            n += 1
        s.commit()
        print(f"Re-synced FAQs for {n} Finuo-Giraffe activities.")
    except Exception as e:
        s.rollback(); print("ERROR:", e); raise
    finally:
        s.close()


if __name__ == "__main__":
    run()
