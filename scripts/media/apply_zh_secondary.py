#!/usr/bin/env python3
"""Fill zh translations for secondary activity fields (what_to_bring/dress_code/covid_measures).

UPDATEs the existing zh activity_translations rows by matching the activity's English
field value against the translated dictionary. Run in the backend container:
    docker cp secondary_zh.json travel_backend:/app/secondary_zh.json
    docker exec travel_backend python /app/apply_zh_secondary.py
"""
import json, os
from sqlalchemy import create_engine, text

eng = create_engine(os.environ["DATABASE_URL"])
D = json.load(open("/app/secondary_zh.json", encoding="utf-8"))


def norm(v):
    return (v or "").strip()


with eng.begin() as cx:
    for field in ("what_to_bring", "dress_code", "covid_measures"):
        dct = {norm(x["en"]): x["zh"] for x in D.get(field, [])}
        n = unm = 0
        rows = cx.execute(text(
            f"select a.id, a.{field} from activities a "
            f"where a.{field} is not null and a.{field} <> '' "
            f"and coalesce((select t.{field} from activity_translations t "
            f"  where t.activity_id=a.id and t.language='zh'),'')=''")).fetchall()
        for aid, en_val in rows:
            zh = dct.get(norm(en_val))
            if zh:
                cx.execute(text(
                    f"update activity_translations set {field}=:z "
                    f"where activity_id=:i and language='zh'"), {"z": zh, "i": aid})
                n += 1
            else:
                unm += 1
        print(f"{field}: updated {n}, unmatched {unm}")
print("done")
