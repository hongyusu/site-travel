#!/usr/bin/env python3
"""Apply 产品特色 / product-feature blocks (bullets + images) to Finuo-Giraffe activities.

Adds activities.product_features JSONB if missing, then sets it per slug from
girafe_features.json: {bullets:[{tag_en,tag_zh,text_en,text_zh}], images:[urls]}.
In place — touches only product_features.

    docker exec travel_backend python /app/apply_girafe_features.py
"""
import json, os, sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.models.activity import Activity

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(os.path.join(here, "girafe_features.json"), encoding="utf-8"))
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE activities ADD COLUMN IF NOT EXISTS product_features JSONB"))
    s = Session()
    try:
        n = 0
        for slug, feat in data.items():
            act = s.query(Activity).filter_by(slug=slug).first()
            if not act:
                print("  ? missing", slug); continue
            act.product_features = feat; n += 1
        s.commit()
        print(f"Set product_features on {n} activities.")
    except Exception as e:
        s.rollback(); print("ERROR:", e); raise
    finally:
        s.close()


if __name__ == "__main__":
    run()
