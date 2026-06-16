#!/usr/bin/env python3
"""Insert Simplified-Chinese (zh) translations produced by the translation workflow.

Run inside the backend container:
    docker cp zh_translations.json travel_backend:/app/zh_translations.json
    docker exec travel_backend python /app/apply_zh.py

Idempotent: only inserts a zh row where one does not already exist. Templated
sub-entities (highlights/includes/faqs/timelines/meeting points) are matched to
their translation by exact English text, so one translation fills every row that
shares that text. Reports any unmatched rows.
"""
import json, os
from sqlalchemy import create_engine, text

eng = create_engine(os.environ["DATABASE_URL"])
D = json.load(open("/app/zh_translations.json", encoding="utf-8"))


def norm(v):
    return (v or "").strip()


with eng.begin() as cx:
    # 1. activities: title/short/description (unique per activity, keyed by id)
    n = 0
    for a in D.get("activities", []):
        exists = cx.execute(text("select 1 from activity_translations where activity_id=:i and language='zh'"),
                            {"i": a["id"]}).first()
        if exists:
            continue
        cx.execute(text("insert into activity_translations(activity_id,language,title,short_description,description) "
                        "values(:i,'zh',:t,:s,:d)"),
                   {"i": a["id"], "t": a["title_zh"], "s": a["short_zh"], "d": a["desc_zh"]})
        n += 1
    print(f"activity_translations inserted: {n}")

    # 2. highlights (match by text)
    hd = {norm(x["en"]): x["zh"] for x in D.get("highlights", [])}
    n = unm = 0
    for hid, t in cx.execute(text("select h.id,h.text from activity_highlights h "
                                  "where not exists (select 1 from activity_highlight_translations tr "
                                  "where tr.highlight_id=h.id and tr.language='zh')")).fetchall():
        zh = hd.get(norm(t))
        if zh:
            cx.execute(text("insert into activity_highlight_translations(highlight_id,language,text) values(:i,'zh',:z)"),
                       {"i": hid, "z": zh}); n += 1
        else:
            unm += 1
    print(f"highlight translations inserted: {n}, unmatched: {unm}")

    # 3. includes (match by item)
    icd = {norm(x["en"]): x["zh"] for x in D.get("includes", [])}
    n = unm = 0
    for iid, item in cx.execute(text("select i.id,i.item from activity_includes i "
                                     "where not exists (select 1 from activity_include_translations tr "
                                     "where tr.include_id=i.id and tr.language='zh')")).fetchall():
        zh = icd.get(norm(item))
        if zh:
            cx.execute(text("insert into activity_include_translations(include_id,language,item) values(:i,'zh',:z)"),
                       {"i": iid, "z": zh}); n += 1
        else:
            unm += 1
    print(f"include translations inserted: {n}, unmatched: {unm}")

    # 4. faqs (match by question+answer)
    fd = {(norm(x["question"]), norm(x["answer"])): (x["question_zh"], x["answer_zh"]) for x in D.get("faqs", [])}
    n = unm = 0
    for fid, q, a in cx.execute(text("select f.id,f.question,f.answer from activity_faqs f "
                                     "where not exists (select 1 from activity_faq_translations tr "
                                     "where tr.faq_id=f.id and tr.language='zh')")).fetchall():
        zh = fd.get((norm(q), norm(a)))
        if zh:
            cx.execute(text("insert into activity_faq_translations(faq_id,language,question,answer) values(:i,'zh',:q,:a)"),
                       {"i": fid, "q": zh[0], "a": zh[1]}); n += 1
        else:
            unm += 1
    print(f"faq translations inserted: {n}, unmatched: {unm}")

    # 5. timelines (match by title+description)
    td = {(norm(x["title"]), norm(x["description"])): (x["title_zh"], x["description_zh"]) for x in D.get("timelines", [])}
    n = unm = 0
    for tid, ti, de in cx.execute(text("select tl.id,tl.title,tl.description from activity_timelines tl "
                                       "where not exists (select 1 from activity_timeline_translations tr "
                                       "where tr.timeline_id=tl.id and tr.language='zh')")).fetchall():
        zh = td.get((norm(ti), norm(de)))
        if zh:
            cx.execute(text("insert into activity_timeline_translations(timeline_id,language,title,description) "
                            "values(:i,'zh',:t,:d)"), {"i": tid, "t": zh[0], "d": zh[1]}); n += 1
        else:
            unm += 1
    print(f"timeline translations inserted: {n}, unmatched: {unm}")

    # 6. meeting points (match by 5-tuple, normalized)
    md = {}
    for x in D.get("meeting_points", []):
        key = tuple(norm(x[k]) for k in ("address", "instructions", "parking_info",
                                         "public_transport_info", "nearby_landmarks"))
        md[key] = x
    n = unm = 0
    for row in cx.execute(text("select m.id,m.address,m.instructions,m.parking_info,m.public_transport_info,m.nearby_landmarks "
                               "from meeting_points m where not exists (select 1 from meeting_point_translations tr "
                               "where tr.meeting_point_id=m.id and tr.language='zh')")).fetchall():
        mid, addr, ins, pk, pt, lm = row
        key = (norm(addr), norm(ins), norm(pk), norm(pt), norm(lm))
        x = md.get(key)
        if x:
            cx.execute(text("insert into meeting_point_translations(meeting_point_id,language,address,instructions,"
                            "parking_info,public_transport_info,nearby_landmarks) "
                            "values(:i,'zh',:a,:ins,:pk,:pt,:lm)"),
                       {"i": mid, "a": x["address_zh"] or addr, "ins": x["instructions_zh"] or None,
                        "pk": x["parking_info_zh"] or None, "pt": x["public_transport_info_zh"] or None,
                        "lm": x["nearby_landmarks_zh"] or None}); n += 1
        else:
            unm += 1
    print(f"meeting_point translations inserted: {n}, unmatched: {unm}")

    # 7. categories (match by name)
    cd = {norm(x["en"]): x["zh"] for x in D.get("categories", [])}
    n = unm = 0
    for cid, name in cx.execute(text("select c.id,c.name from categories c "
                                     "where not exists (select 1 from category_translations tr "
                                     "where tr.category_id=c.id and tr.language='zh')")).fetchall():
        zh = cd.get(norm(name))
        if zh:
            cx.execute(text("insert into category_translations(category_id,language,name) values(:i,'zh',:z)"),
                       {"i": cid, "z": zh}); n += 1
        else:
            unm += 1
    print(f"category translations inserted: {n}, unmatched: {unm}")

    # 8. destinations (match by name)
    dd = {norm(x["en"]): x["zh"] for x in D.get("destinations", [])}
    n = unm = 0
    for did, name in cx.execute(text("select d.id,d.name from destinations d "
                                     "where not exists (select 1 from destination_translations tr "
                                     "where tr.destination_id=d.id and tr.language='zh')")).fetchall():
        zh = dd.get(norm(name))
        if zh:
            cx.execute(text("insert into destination_translations(destination_id,language,name) values(:i,'zh',:z)"),
                       {"i": did, "z": zh}); n += 1
        else:
            unm += 1
    print(f"destination translations inserted: {n}, unmatched: {unm}")

print("done")
