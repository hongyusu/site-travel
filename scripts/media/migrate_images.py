#!/usr/bin/env python3
"""Rewrite all image URLs in the DB to self-hosted /media/ paths.

Run inside the backend container (needs DATABASE_URL):
    docker cp /tmp/img_manifest.json travel_backend:/app/img_manifest.json
    docker cp /tmp/china_images.json travel_backend:/app/china_images.json
    docker exec travel_backend python /app/migrate_images.py

1. Generic: every external URL present in the manifest -> /media/stock/<hash>.<ext>.
2. China override: the 8 China tours get real site-finuo photos for their
   activity_images (full gallery, hero first), timeline step images, and the four
   linked destinations (Anhui/Suzhou/Shanghai/Hangzhou) get a hero photo.
"""
import json, os
from sqlalchemy import create_engine, text

eng = create_engine(os.environ["DATABASE_URL"])
manifest = json.load(open("/app/img_manifest.json"))
china = json.load(open("/app/china_images.json"))

with eng.begin() as cx:
    cols = [("activity_images", "url"), ("activity_timelines", "image_url"),
            ("destinations", "image_url"), ("meeting_point_photos", "url"),
            ("review_images", "url"), ("vendors", "logo_url")]
    n = miss = 0
    for tbl, col in cols:
        for rid, url in cx.execute(
                text(f"select id,{col} from {tbl} where {col} like 'http%'")).fetchall():
            if url in manifest:
                cx.execute(text(f"update {tbl} set {col}=:u where id=:i"),
                           {"u": manifest[url], "i": rid}); n += 1
            else:
                miss += 1
    print(f"generic: replaced {n}, left-unmapped {miss}")

    for slug, gallery in china["activities"].items():
        r = cx.execute(text("select id from activities where slug=:s"), {"s": slug}).first()
        if not r:
            print("MISSING activity", slug); continue
        aid = r[0]
        cx.execute(text("delete from activity_images where activity_id=:a"), {"a": aid})
        for i, p in enumerate(gallery):
            cx.execute(text(
                "insert into activity_images(activity_id,url,alt_text,is_primary,is_hero,order_index) "
                "values(:a,:u,:alt,:pri,:hero,:o)"),
                {"a": aid, "u": p, "alt": f"{slug} image {i+1}",
                 "pri": i == 0, "hero": i == 0, "o": i})
        tls = cx.execute(text(
            "select id from activity_timelines where activity_id=:a order by order_index"),
            {"a": aid}).fetchall()
        L = len(gallery); idxs = [0, L // 3, (2 * L) // 3]
        for k, (tid,) in enumerate(tls):
            cx.execute(text("update activity_timelines set image_url=:u where id=:i"),
                       {"u": gallery[idxs[k] if k < len(idxs) else k % L], "i": tid})
    for ds, p in china["destinations"].items():
        cx.execute(text("update destinations set image_url=:u where slug=:s"), {"u": p, "s": ds})
    print("china overrides applied")
