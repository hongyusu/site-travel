#!/usr/bin/env python3
"""Seed 20-30 customer reviews for each Finuo-Giraffe European tour (idempotent).

Region-aware bilingual reviews (Chinese reviewers write zh, international write
en), weighted ratings, varied dates/helpful counts, and ~1/3 with a photo drawn
from the tour's own gallery. Unlike the Finuo Oy seeding, this RECOMPUTES each
activity's average_rating/total_reviews from the seeded reviews, so the new
listings are fully consistent.

Run inside the backend container (after seed_girafe_tours.py):
    docker exec travel_backend python /app/seed_girafe_reviews.py
Idempotent: skips activities that already have reviews.
"""

import os, json, random
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, text

random.seed(20260624)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate")
engine = create_engine(DATABASE_URL)
VENDOR_COMPANY = "Finuo-Giraffe"
PW_HASH = "$2b$12$TxjAN.QLj4nory7k.VFcF.SSwEEM8e1bPYaVVf0vgMQ3QpI.YM0Cy"
BASE_DATE = datetime(2025, 5, 1, tzinfo=timezone.utc)
HELPFUL = [0,0,1,2,2,3,4,5,6,8,10,12,15,18,22,28,35,42]

CHINESE = [("张伟","zhangwei"),("李娜","lina"),("王芳","wangfang"),("刘洋","liuyang"),
 ("陈静","chenjing"),("杨帆","yangfan"),("赵磊","zhaolei"),("孙琳","sunlin"),("周婷","zhouting"),
 ("吴昊","wuhao"),("郑爽","zhengshuang"),("林峰","linfeng"),("黄蕾","huanglei"),("徐明","xuming"),
 ("何颖","heying"),("高翔","gaoxiang"),("马丽","mali"),("朱倩","zhuqian"),("胡军","hujun"),("罗梅","luomei"),
 ("邓超","dengchao"),("冯雪","fengxue"),("曾敏","zengmin"),("彭勇","pengyong"),("蒋雯","jiangwen"),
 ("韩磊","hanlei"),("唐丽","tangli"),("范晓","fanxiao"),("董伟","dongwei"),("萧涵","xiaohan")]
INTL = [("Sarah Thompson","sarah.t"),("James Wilson","james.w"),("Emma Becker","emma.b"),
 ("Luca Rossi","luca.r"),("Sophie Martin","sophie.m"),("David Kim","david.k"),("Olivia Brown","olivia.b"),
 ("Daniel Lee","daniel.l"),("Hannah Schmidt","hannah.s"),("Thomas Anderson","thomas.a"),
 ("Yuki Tanaka","yuki.t"),("Min-jun Park","minjun.p"),("Laura Garcia","laura.g"),
 ("Niklas Berg","niklas.b"),("Chloe Moreau","chloe.m"),("Marco Bianchi","marco.b")]

REGION_ZH = {
 "france-italy-switzerland":[("一次玩三国超值","法意瑞一条线把欧洲精华都走遍了，巴黎的浪漫、瑞士的雪山、意大利的文艺复兴，导游讲解很专业，行程紧凑但不累。"),
  ("瑞士段太惊艳了","少女峰和日内瓦湖的风景美到窒息，金色山口列车一定要体验。三国连游性价比很高，住的都是市中心好酒店。"),
  ("文艺复兴之旅","从米兰到威尼斯再到佛罗伦萨、罗马，一路都是艺术与历史，导游知识渊博，五渔村和托斯卡纳山城更是惊喜。"),
  ("单程不走回头路","巴黎进罗马出，一路向南深度游，行程设计很合理，不浪费时间，一价全含没有强制购物，省心。"),
  ("带父母玩得很开心","三国行程节奏适中，老人也能跟上，司导一路照顾周到，酒店和餐食都不错，全家都很满意。"),
  ("欧洲初体验首选","第一次来欧洲就选了法意瑞，经典中的经典，该看的都看了，导游推荐的当地美食也很地道。")],
 "france":[("巴黎深度游很惊喜","卢浮宫有专业讲解师带着看，完全不一样的体验，凡尔赛宫和塞纳河游船都很棒，三天把巴黎精华玩透了。"),
  ("浪漫之都名不虚传","从卢浮宫到埃菲尔铁塔再到香榭丽舍，导游把巴黎的艺术与历史讲得生动有趣，行程轻松惬意。"),
  ("普罗旺斯太美了","薰衣草和蔚蓝海岸的风景像画一样，南法的小镇悠闲浪漫，导游很贴心，节奏刚刚好。"),
  ("诺曼底圣山震撼","圣米歇尔山真的太壮观了，涨潮时如海上城堡，导游讲解历史很到位，小团体验很自在。"),
  ("艺术爱好者必去","卢浮宫的精讲让人受益匪浅，奥斯曼大街逛街也很尽兴，巴黎的每个角落都充满魅力。"),
  ("自由与深度兼顾","行程既有深度讲解又留了自由活动时间，很人性化，住宿位置好，出行方便。")],
 "switzerland-alps":[("阿尔卑斯太治愈了","少女峰、卢塞恩、苏黎世一路雪山湖泊，空气清新，金色山口观光列车的风景一辈子难忘。"),
  ("瑞士环线很完美","环线设计把瑞士精华串起来，铁力士雪山和湖区都很美，导游专业，住宿干净舒适。"),
  ("火车控的天堂","瑞士的观光列车体验太棒了，沿途风景美不胜收，行程安排合理，节奏轻松。"),
  ("风景如明信片","每一站都美得像明信片，琉森湖、廊桥、雪山，随手一拍都是大片，强烈推荐。"),
  ("德瑞奥连游超值","德国瑞士奥地利一次玩遍，新天鹅堡、少女峰都很震撼，导游讲解细致，行程顺畅。"),
  ("亲子游好选择","瑞士安全又干净，风景好节奏慢，带孩子来阿尔卑斯山看雪山湖泊，全家都很开心。")],
 "italy":[("意大利一地深度","罗马、佛罗伦萨、威尼斯、米兰一路艺术与美食，斗兽场和水城威尼斯太震撼了，导游讲解很专业。"),
  ("文艺复兴的盛宴","佛罗伦萨的圣母百花大教堂、乌菲兹的艺术氛围，加上托斯卡纳的田园风光，意大利太迷人了。"),
  ("五渔村和西西里","五渔村的悬崖渔村太上镜了，西西里段更是惊喜，行程丰富，住宿和餐食都很赞。"),
  ("多洛米蒂太美","多洛米蒂的雪山和湖泊美到不真实，小团深度游很自在，导游找的机位都很出片。"),
  ("美食与艺术兼得","意大利的披萨、冰淇淋、咖啡配上各地的艺术古迹，这趟旅程太满足了，强烈推荐。"),
  ("罗马假日圆梦","许愿池、斗兽场、梵蒂冈，跟着导游深度游罗马，历史故事讲得引人入胜，难忘的旅程。")],
 "iceland-region":[("冰岛风光太震撼","黄金圈、瀑布、冰川、黑沙滩，每一处都是大自然的鬼斧神工，小团深度游很自在，司导很专业。"),
  ("追极光圆梦了","运气很好看到了绚烂的极光，蓝湖温泉泡着太舒服，冰岛的冬天像童话世界，难忘。"),
  ("环岛自驾般体验","环岛把冰岛精华走遍，冰河湖的浮冰太美了，导游兼司机经验丰富，安全又省心。"),
  ("地球上的另一个星球","间歇泉、火山地貌、冰川徒步，冰岛的景色独一无二，行程安排紧凑而充实。"),
  ("小团体验超棒","4-8人的小团很自在，想停就停拍照，司导对每个景点都了如指掌，强烈推荐。"),
  ("此生必去之地","冰岛的自然太纯粹了，瀑布和冰川震撼心灵，虽然路途遥远但完全值得。")],
 "norway-fjords":[("峡湾风光绝美","挪威的峡湾深邃壮丽，坐船游峡湾的体验太震撼了，沿途瀑布雪山，风景一流。"),
  ("罗弗敦群岛太美","罗弗敦的渔村和雪山倒影像仙境，半自助行程很自由，司导很贴心，出片率超高。"),
  ("北欧四国连游","丹麦挪威瑞典芬兰一路玩下来，峡湾、古城、童话小镇都很精彩，行程丰富。"),
  ("特罗姆瑟追极光","北极圈内追极光太刺激了，雪景配极光美到流泪，导游经验丰富会找最佳位置。"),
  ("挪威缩影之旅","高山峡湾火车加游船，挪威的精华一次体验，风景美得让人忘记呼吸，强烈推荐。"),
  ("宁静而壮美","峡湾的宁静与壮美让人心旷神怡，住宿和交通安排得当，是一次放松身心的旅程。")],
 "spain-portugal":[("加那利群岛惊艳","兰萨罗特和特内里费的火山地貌太特别了，海岛风光配上宜人气候，度假感十足。"),
  ("阳光海岛之旅","加那利群岛冬天也温暖如春，火山、沙滩、星空，行程轻松惬意，很适合度假。"),
  ("独特的火山岛","提曼法亚火山公园太震撼了，月球般的地貌让人惊叹，导游讲解专业，安排周到。"),
  ("海岛风情满分","群岛各有特色，跳岛游很丰富，美食和风景都很赞，是一次完美的海岛假期。"),
  ("西葡阳光灿烂","伊比利亚半岛的热情与阳光令人难忘，行程节奏舒适，住宿位置好，强烈推荐。"),
  ("度假首选","加那利的气候太舒服了，海滩和火山景观兼得，全家度假的好选择。")],
}
GENERIC_ZH = [("非常难忘的欧洲之旅","整个行程安排得井井有条，导游专业又热情，每个细节都照顾到了，强烈推荐。"),
 ("超出预期的体验","本来没抱太高期待，结果惊喜连连，导游知识渊博讲解生动，全程都很愉快。"),
 ("物超所值一价全含","这个价格能有这样的体验真的很值，住宿和餐食都不错，没有强制购物，省心。"),
 ("导游非常专业","司导对当地历史文化了如指掌，讲解风趣幽默，还帮我们拍了很多美照，点赞。"),
 ("行程安排很合理","节奏不赶不慢，该看的都看到了，还有自由活动时间，很人性化。"),
 ("适合全家出游","带着老人孩子一起，导游照顾得很周到，大家都玩得很开心。"),
 ("风景美到窒息","沿途的风景太美了，随手一拍都是大片，留下了满满的回忆。"),
 ("服务很贴心","从接送到讲解再到餐食安排，处处都能感受到用心。"),
 ("会推荐给朋友","玩得太开心了，已经推荐给身边好几个朋友，靠谱专业有温度。"),
 ("难得的深度游","不是走马观花，而是真正深入体验当地文化，收获很多。"),
 ("性价比之王","对比了好几家，这个行程性价比最高，体验却一点不打折。"),
 ("第一次跟团很满意","第一次跟这种团体验非常好，导游能照顾到每个人，很自在。"),
 ("照片拍到手软","每个景点导游都知道最佳拍照点，回来相册都装不下了。"),
 ("轻松省心的旅行","全程不用操心，跟着走就行，住宿交通都安排妥当。"),
 ("住宿超出预期","酒店都在市中心，干净舒适位置好，晚上还能自己出去逛逛。"),
 ("中文司导太方便","全程中文服务沟通无障碍，导游还推荐了很多当地美食和小贴士。"),
 ("无强制购物点赞","全程没有任何强制购物，导游专心带团，体验非常纯粹。"),
 ("值得再来一次","这趟玩得意犹未尽，下次还想参加他们家其他线路。"),
 ("惊喜满满","每一天都有新鲜的体验，旅途非常愉快，超出预期。"),
 ("欧洲游首选","无论风景服务还是行程安排都很棒，欧洲游就选他家。")]
GENERIC_EN = [("An unforgettable European trip","Beautifully organized from start to finish. Our guide was knowledgeable and warm, and every detail was taken care of. Highly recommend!"),
 ("Exceeded all expectations","The scenery was stunning and the guide's stories brought everything to life. A wonderful journey across Europe."),
 ("Great value, all-inclusive","Outstanding experience for the price — comfortable hotels, smooth transport, no forced shopping. Would book again."),
 ("Our guide made the trip","Passionate and deeply knowledgeable about the local history and culture, friendly and patient throughout."),
 ("Perfectly paced itinerary","Never felt rushed. We saw all the highlights and still had free time. Thoughtfully planned and very smooth."),
 ("Great for families","Travelled with kids and grandparents — everyone had a fantastic time and the guide looked after us all."),
 ("Breathtaking scenery","Every view looked like a postcard. One of the highlights of our whole trip."),
 ("A truly authentic experience","Felt like seeing the real Europe, not a tourist trap. The local insight made all the difference."),
 ("Smooth and stress-free","Hotels, transport and tickets all handled. We just showed up and enjoyed."),
 ("Highlight of our holiday","Out of everything we did, this stood out. Well-guided, beautiful, full of memories."),
 ("Would absolutely recommend","Seamless and professional from booking to the last day. Already told friends back home."),
 ("Central hotels, great location","The hotels were right in the city centre, clean and comfortable, easy to explore in the evenings."),
 ("Wonderful Chinese-speaking guide","Communication was effortless and the guide shared great food tips and local advice."),
 ("No forced shopping — refreshing","Not a single forced shopping stop; the guide focused entirely on the experience."),
 ("Stunning and well run","A lot of care went into this — beautiful locations, an excellent guide and an itinerary that just worked."),
 ("Memories to last a lifetime","From the landscapes to the little details, this trip was simply special.")]


def ensure_users(conn, reviewers):
    ids = []
    for name, local in reviewers:
        email = f"{local}@reviewers.finuo.fi"
        r = conn.execute(text("SELECT id FROM users WHERE email=:e"), {"e": email}).first()
        if r:
            ids.append(r[0])
        else:
            ids.append(conn.execute(text(
                "INSERT INTO users (email,password_hash,full_name,role,email_verified,is_active) "
                "VALUES (:e,:p,:n,'CUSTOMER',true,true) RETURNING id"),
                {"e": email, "p": PW_HASH, "n": name}).scalar())
    return ids


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    slug_region = {t["slug"]: t["region"]["slug"] for t in json.load(open(os.path.join(here, "girafe_tours.json")))}
    with engine.begin() as conn:
        for tbl in ("users", "reviews", "review_images"):
            conn.execute(text(f"SELECT setval(pg_get_serial_sequence('{tbl}','id'),"
                              f"COALESCE((SELECT MAX(id) FROM {tbl}),0)+1,false)"))
        zh_users = ensure_users(conn, CHINESE)
        en_users = ensure_users(conn, INTL)
        vid = conn.execute(text("SELECT id FROM vendors WHERE company_name=:c"), {"c": VENDOR_COMPANY}).scalar()
        if not vid:
            print("Finuo-Giraffe vendor not found — run seed_girafe_tours.py first."); raise SystemExit(1)
        acts = conn.execute(text("SELECT id, slug FROM activities WHERE vendor_id=:v ORDER BY id"), {"v": vid}).fetchall()
        total = 0
        for a in acts:
            if conn.execute(text("SELECT count(*) FROM reviews WHERE activity_id=:a"), {"a": a.id}).scalar() > 0:
                continue
            region = slug_region.get(a.slug, "france")
            imgs = [r[0] for r in conn.execute(text("SELECT url FROM activity_images WHERE activity_id=:a"), {"a": a.id}).fetchall()]
            n = random.randint(20, 30)
            n_zh = round(n * 0.72); n_en = n - n_zh
            zh_pool = REGION_ZH.get(region, []) + GENERIC_ZH
            zh_pick = random.sample(zh_pool, min(n_zh, len(zh_pool)))
            en_pick = random.sample(GENERIC_EN, min(n_en, len(GENERIC_EN)))
            items = ([(c, u) for c, u in zip(zh_pick, random.sample(zh_users, len(zh_pick)))] +
                     [(c, u) for c, u in zip(en_pick, random.sample(en_users, len(en_pick)))])
            random.shuffle(items)
            for (title, comment), uid in items:
                rating = random.choices([5, 4, 3], weights=[7, 2, 1])[0]
                created = BASE_DATE + timedelta(days=random.randint(0, 410), hours=random.randint(0, 23), minutes=random.randint(0, 59))
                rid = conn.execute(text(
                    "INSERT INTO reviews (user_id,activity_id,vendor_id,rating,title,comment,is_verified_booking,helpful_count,created_at)"
                    " VALUES (:u,:a,:v,:r,:t,:c,:vb,:h,:ts) RETURNING id"),
                    {"u": uid, "a": a.id, "v": vid, "r": rating, "t": title, "c": comment,
                     "vb": random.random() < 0.85, "h": random.choice(HELPFUL), "ts": created}).scalar()
                if imgs and random.random() < 0.32:
                    conn.execute(text("INSERT INTO review_images (review_id,url) VALUES (:r,:u)"),
                                 {"r": rid, "u": random.choice(imgs)})
                total += 1
        # recompute aggregates from actual reviews (Finuo-Giraffe activities only)
        conn.execute(text(
            "UPDATE activities a SET total_reviews=s.cnt, average_rating=s.avg FROM "
            "(SELECT activity_id, COUNT(*) cnt, ROUND(AVG(rating)::numeric,1) avg FROM reviews GROUP BY activity_id) s "
            "WHERE a.id=s.activity_id AND a.vendor_id=:v"), {"v": vid})
        print(f"Inserted {total} reviews across {len(acts)} Finuo-Giraffe activities; aggregates recomputed.")
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT a.title, a.total_reviews, a.average_rating FROM activities a "
            "JOIN vendors v ON v.id=a.vendor_id WHERE v.company_name=:c ORDER BY a.id LIMIT 8"), {"c": VENDOR_COMPANY}).fetchall()
        for r in rows:
            print(f"  {r.title[:48]:<48} {r.total_reviews} reviews, {r.average_rating}★")


if __name__ == "__main__":
    main()
