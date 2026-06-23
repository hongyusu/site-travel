#!/usr/bin/env python3
"""Seed realistic customer reviews for the Finuo provider's activities (vendor 14).

The 8 Finuo China tours (activity ids 72-79) shipped with curated
average_rating/total_reviews aggregates but ZERO actual review rows, so the
reviews section rendered "No reviews yet" under a high rating. This seeds a
believable set of mostly-Chinese (plus some English) reviews per tour, with
tour-specific flavour, weighted ratings, varied dates/helpful counts, and a
few review photos taken from each activity's own image set.

The curated activities.average_rating / total_reviews aggregates are left
UNCHANGED (marketplace norm: header shows the total, the list shows a page).

Run inside the backend container:
    docker exec travel_backend python /app/seed_finuo_reviews.py
Idempotent: skips any activity that already has reviews.
"""

import os
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, text

random.seed(20260623)  # reproducible content/ratings

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate"
)
engine = create_engine(DATABASE_URL)

VENDOR_ID = 14
# Reuse an existing valid bcrypt hash; these accounts are review authors only.
PW_HASH = "$2b$12$TxjAN.QLj4nory7k.VFcF.SSwEEM8e1bPYaVVf0vgMQ3QpI.YM0Cy"

# (full_name, email-local-part)
CHINESE_REVIEWERS = [
    ("张伟", "zhangwei"), ("李娜", "lina"), ("王芳", "wangfang"), ("刘洋", "liuyang"),
    ("陈静", "chenjing"), ("杨帆", "yangfan"), ("赵磊", "zhaolei"), ("孙琳", "sunlin"),
    ("周婷", "zhouting"), ("吴昊", "wuhao"), ("郑爽", "zhengshuang"), ("林峰", "linfeng"),
    ("黄蕾", "huanglei"), ("徐明", "xuming"), ("何颖", "heying"), ("高翔", "gaoxiang"),
    ("马丽", "mali"), ("朱倩", "zhuqian"), ("胡军", "hujun"), ("罗梅", "luomei"),
]
INTL_REVIEWERS = [
    ("Sarah Thompson", "sarah.t"), ("James Wilson", "james.w"), ("Emma Becker", "emma.b"),
    ("Luca Rossi", "luca.r"), ("Sophie Martin", "sophie.m"), ("David Kim", "david.k"),
    ("Olivia Brown", "olivia.b"), ("Daniel Lee", "daniel.l"), ("Hannah Schmidt", "hannah.s"),
    ("Thomas Anderson", "thomas.a"), ("Yuki Tanaka", "yuki.t"), ("Min-jun Park", "minjun.p"),
]

# Tour-specific Chinese reviews keyed by activity id.
TOUR_ZH = {
    72: [  # Huangshan (Yellow Mountain)
        ("黄山日出太震撼了", "在光明顶看日出，云海翻腾，太阳跃出地平线的那一刻全场都安静了。三天行程安排得很合理，导游对每个观景台都了如指掌，强烈推荐！"),
        ("云海和迎客松名不虚传", "运气很好赶上了云海，迎客松前拍了好多照片。爬山虽然累，但缆车衔接得当，导游一路讲解黄山的地质和典故，很长知识。"),
        ("三天两晚刚刚好", "第一次爬黄山，三天的节奏不赶，山上住了一晚看了日落又看日出。住宿和餐食都比预想的好，向导非常专业。"),
        ("值得一生去一次", "黄山的奇松怪石云海温泉果然名副其实。导游提前帮我们规划好体力分配，老人小孩都能跟上，下山还泡了温泉，太舒服了。"),
        ("摄影爱好者的天堂", "为了拍云海特意来的，导游带我们到最佳机位，凌晨就出发占位。三天拍到了日出、晚霞和星空，不虚此行。"),
    ],
    73: [  # Huizhou ancient villages
        ("粉墙黛瓦美如画", "宏村西递的徽派建筑太美了，马头墙、月沼、古祠堂，每个角落都像水墨画。导游讲徽商和徽文化的故事很生动。"),
        ("走进了水墨江南", "古村落保存得非常完整，清晨的宏村安静又有韵味。三天慢慢逛不像赶鸭子，导游还推荐了当地的臭鳜鱼和毛豆腐。"),
        ("徽文化底蕴深厚", "不只是看房子，导游把徽州的历史、雕刻、风水都讲透了，孩子听得津津有味。古村的写生氛围特别浓。"),
        ("适合慢节奏深度游", "避开了人潮，在西递的巷子里慢慢走，喝茶看雕梁画栋。住的民宿也是老宅改的，体验很地道。"),
        ("三雕艺术令人惊叹", "木雕石雕砖雕精美到不可思议，导游一处处带我们看细节。徽州的美需要慢慢品，这趟很值。"),
    ],
    74: [  # Mount Qiyun
        ("道教名山清幽宁静", "齐云山人不多，丹霞地貌配上道观特别出片。月华街的氛围很特别，导游讲道教文化深入浅出。"),
        ("丹霞地貌很惊艳", "红色的山岩配上云雾仙气十足，香炉峰、太素宫都很值得一看。三天行程轻松，适合放空。"),
        ("远离喧嚣的好去处", "比起热门景点这里清净太多了，登山步道平缓，老人也走得动，导游耐心又专业。"),
        ("小众但惊喜", "原本没抱太大期待，结果齐云山的山水道观让人很惊喜。空气好，节奏慢，身心都放松了。"),
        ("适合静心的旅程", "在月华街住了一晚，清晨的云雾缭绕太美了。导游对当地典故信手拈来，三天下来收获满满。"),
    ],
    75: [  # Southern Anhui & Jingxian
        ("皖南乡村太治愈了", "查济古村、桃花潭，处处是田园风光。三天慢游远离城市喧嚣，导游带我们体验了宣纸制作，很有意思。"),
        ("桃花潭名不虚传", "李白笔下的桃花潭真的很美，乘船游潭很惬意。皖南的油菜花和古村落配在一起像画一样。"),
        ("深度体验皖南文化", "不只是看风景，还参观了宣纸作坊，了解了传统工艺。导游知识丰富，行程安排很用心。"),
        ("田园风光美不胜收", "查济的老桥流水人家太有味道了，随手一拍都是大片。三天的乡村慢生活让人不想回城。"),
        ("适合摄影和写生", "皖南的山水古村是创作的天堂，光线和构图都绝了，导游带我们找了很多隐藏机位。"),
    ],
    76: [  # Suzhou classical gardens
        ("移步换景的园林艺术", "拙政园、留园真是步步是景，导游把造园的巧思讲得很透。三天逛了好几个园子，还游了古城河。"),
        ("江南园林甲天下", "网师园的精致、拙政园的开阔各有韵味。苏州的小桥流水太治愈了，导游推荐的苏帮菜也很赞。"),
        ("古典园林的极致美学", "亭台楼阁假山流水，处处见匠心。导游讲解了借景、对景的手法，再看园子完全不一样了。"),
        ("苏州古城韵味十足", "白天逛园林，晚上逛平江路，三天把苏州的精华都体验了。导游很专业，节奏不赶。"),
        ("园林控的天堂", "作为园林爱好者太满足了，每个园子的设计理念导游都讲得很清楚，还赶上了评弹表演，很地道。"),
    ],
    77: [  # Hangzhou West Lake
        ("上有天堂下有苏杭", "西湖三天怎么逛都不腻，断桥、苏堤、雷峰塔，导游讲了很多白娘子的传说，还去龙井村喝了正宗龙井。"),
        ("西湖的美无法形容", "清晨的苏堤烟雾朦胧太美了，游船看三潭印月很惬意。灵隐寺也很值得，导游讲解很到位。"),
        ("龙井茶香醉人", "在龙井村体验了采茶和炒茶，喝着明前龙井看茶园太惬意了。三天行程文化和风景兼顾。"),
        ("江南水乡的诗意", "西湖十景慢慢逛，雷峰夕照、平湖秋月各有味道。导游对杭州历史如数家珍，很涨知识。"),
        ("灵隐寺很有灵气", "灵隐寺的古木和佛像让人心静，飞来峰的石刻也很震撼。三天节奏舒服，住宿位置也好。"),
    ],
    78: [  # Suzhou & Hangzhou combo
        ("一次玩转苏杭", "苏州园林加杭州西湖，江南精华一网打尽。三天行程衔接顺畅，导游对两地都很熟，强烈推荐。"),
        ("江南水乡梦之旅", "从苏州的园林到杭州的西湖，一路都是诗情画意。高铁衔接很方便，导游安排得很贴心。"),
        ("苏杭双城太值了", "时间有限想两个都去，这个行程刚刚好。苏帮菜和杭帮菜都尝了，风景和美食双丰收。"),
        ("经典江南线路", "园林、古镇、西湖、龙井，三天体验非常丰富。节奏把控得好不会太赶，老人也适合。"),
        ("性价比超高的行程", "一次行程玩两座名城，导游专业讲解到位，住宿和交通都省心，非常推荐给第一次来江南的朋友。"),
    ],
    79: [  # Shanghai
        ("魔都三天意犹未尽", "外滩的夜景太震撼了，万国建筑配上对岸的陆家嘴。豫园、田子坊、南京路都逛了，导游对上海了如指掌。"),
        ("古典与现代的碰撞", "上午逛豫园老城厢，下午看陆家嘴摩天楼，上海的反差感太迷人了。三天行程丰富又不赶。"),
        ("外滩夜景一绝", "夜游黄浦江看两岸灯光秀太美了。导游讲了很多老上海的故事，石库门、老洋房都很有味道。"),
        ("逛吃逛吃太满足", "南京路、城隍庙、田子坊一路逛吃，小笼包生煎都尝了个遍，导游推荐的本地小馆很地道。"),
        ("第一次来上海很完美", "三天把上海的经典都打卡了，外滩、东方明珠、豫园、武康路，导游贴心又专业，行程安排很合理。"),
    ],
}

GENERIC_ZH = [
    ("非常难忘的旅程", "整个行程安排得井井有条，导游专业又热情，每个细节都照顾到了。强烈推荐给计划出行的朋友。"),
    ("超出预期的体验", "本来没抱太高期待，结果惊喜连连。导游知识渊博，讲解生动，全程都很愉快。"),
    ("物超所值", "这个价格能有这样的体验真的很值，住宿和餐食都不错，导游服务到位，会推荐给朋友。"),
    ("导游非常专业", "导游对当地历史文化了如指掌，讲解风趣幽默，还帮我们拍了很多美照，点赞！"),
    ("行程安排很合理", "三天节奏不赶不慢，该看的都看到了，还有自由活动时间，很人性化。"),
    ("适合全家出游", "带着老人孩子一起，导游照顾得很周到，大家都玩得很开心，是一次美好的家庭旅行。"),
    ("风景美到窒息", "沿途的风景太美了，随手一拍都是大片，这趟来得太值了，留下了满满的回忆。"),
    ("服务很贴心", "从接送到讲解再到餐食安排，处处都能感受到用心，有什么需求导游都尽量满足。"),
    ("会再来第二次", "玩得太开心了，下次还想再参加他们家的行程，靠谱、专业、有温度。"),
    ("难得的深度游", "不是走马观花，而是真正深入体验当地文化，收获很多，强烈推荐。"),
    ("性价比之王", "对比了好几家，这个行程性价比最高，体验却一点不打折，非常满意。"),
    ("第一次参团很满意", "第一次跟这种小团体验非常好，人不多，导游能照顾到每个人，很自在。"),
    ("照片拍到手软", "每个景点导游都知道最佳拍照点，回来相册都装不下了，朋友圈被赞爆。"),
    ("轻松省心的旅行", "全程不用操心，跟着走就行，住宿交通都安排妥当，难得的放松之旅。"),
    ("值得推荐", "无论是风景、服务还是行程安排都很棒，已经推荐给身边好几个朋友了。"),
    ("惊喜满满的三天", "每一天都有新鲜的体验，导游还准备了一些小惊喜，旅途非常愉快。"),
]

GENERIC_EN = [
    ("An unforgettable trip", "Everything was beautifully organized from start to finish. Our guide was knowledgeable and warm, and every detail was taken care of. Highly recommend!"),
    ("Exceeded all expectations", "I didn't expect much but was blown away. The scenery was stunning and the guide's stories brought everything to life. A wonderful three days."),
    ("Incredible value", "For this price the experience was outstanding. Comfortable accommodation, great food, and a guide who genuinely cared. Would book again."),
    ("Our guide made the trip", "Our guide was passionate and deeply knowledgeable about the local history and culture. Friendly, patient, and even took great photos for us."),
    ("Perfectly paced itinerary", "Three days that never felt rushed. We saw all the highlights and still had time to wander. Thoughtfully planned and very smooth."),
    ("Great for families", "Travelled with kids and grandparents and everyone had a fantastic time. The guide looked after everyone wonderfully."),
    ("Breathtaking scenery", "The landscapes were jaw-dropping — every photo looks like a postcard. One of the highlights of our entire China trip."),
    ("A truly authentic experience", "This felt like seeing the real China, not a tourist trap. The local insight and small personal touches made all the difference."),
    ("Smooth and stress-free", "Transport, hotels, meals — all handled. We just showed up and enjoyed. A genuinely relaxing way to travel."),
    ("Highlight of our holiday", "Out of everything we did, this stood out. Well-guided, beautiful, and packed with memories we'll keep for years."),
    ("Would absolutely recommend", "From booking to the final day, everything was seamless and professional. Already recommended it to friends back home."),
    ("Beautiful and well-run", "A lot of care clearly went into this. Stunning locations, excellent guide, and an itinerary that just worked."),
]

# Target review counts per activity (kept < 20 so all render without the
# load-more pager); loosely scaled by the curated total_reviews.
TARGETS = {72: 18, 73: 13, 74: 10, 75: 9, 76: 16, 77: 15, 78: 14, 79: 18}

HELPFUL_CHOICES = [0, 0, 1, 2, 2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 28, 35]
BASE_DATE = datetime(2025, 4, 1, tzinfo=timezone.utc)


def ensure_users(conn, reviewers):
    """Insert reviewer users if missing; return list of their ids in order."""
    ids = []
    for full_name, local in reviewers:
        email = f"{local}@reviewers.finuo.fi"
        row = conn.execute(text("SELECT id FROM users WHERE email = :e"), {"e": email}).first()
        if row:
            ids.append(row[0])
            continue
        new_id = conn.execute(
            text("INSERT INTO users (email, password_hash, full_name, role, email_verified, is_active) "
                 "VALUES (:e, :p, :n, 'CUSTOMER', true, true) RETURNING id"),
            {"e": email, "p": PW_HASH, "n": full_name},
        ).scalar()
        ids.append(new_id)
    return ids


def main() -> None:
    """Seed reviews (with a few photos) for the Finuo activities."""
    with engine.begin() as conn:
        # Fix stale sequences (DB was restored from a backup).
        for table in ("users", "reviews", "review_images"):
            conn.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                f"COALESCE((SELECT MAX(id) FROM {table}), 0) + 1, false)"
            ))

        zh_user_ids = ensure_users(conn, CHINESE_REVIEWERS)
        en_user_ids = ensure_users(conn, INTL_REVIEWERS)

        total_inserted = 0
        for aid, target in TARGETS.items():
            if conn.execute(
                text("SELECT count(*) FROM reviews WHERE activity_id = :a"), {"a": aid}
            ).scalar() > 0:
                print(f"  activity {aid}: already has reviews, skipping.")
                continue

            images = [r[0] for r in conn.execute(
                text("SELECT url FROM activity_images WHERE activity_id = :a ORDER BY id"),
                {"a": aid},
            ).fetchall()]

            n_zh = round(target * 0.75)
            n_en = target - n_zh
            zh_content = random.sample(TOUR_ZH[aid] + GENERIC_ZH, n_zh)
            en_content = random.sample(GENERIC_EN, n_en)
            zh_users = random.sample(zh_user_ids, n_zh)
            en_users = random.sample(en_user_ids, n_en)

            items = list(zip(zh_content, zh_users)) + list(zip(en_content, en_users))
            random.shuffle(items)

            for (title, comment), uid in items:
                rating = random.choices([5, 4, 3], weights=[7, 2, 1])[0]
                created = BASE_DATE + timedelta(
                    days=random.randint(0, 440), hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )
                rid = conn.execute(
                    text("INSERT INTO reviews "
                         "(user_id, activity_id, vendor_id, rating, title, comment, "
                         " is_verified_booking, helpful_count, created_at) "
                         "VALUES (:u, :a, :v, :r, :t, :c, :vb, :h, :ts) RETURNING id"),
                    {"u": uid, "a": aid, "v": VENDOR_ID, "r": rating, "t": title,
                     "c": comment, "vb": random.random() < 0.85,
                     "h": random.choice(HELPFUL_CHOICES), "ts": created},
                ).scalar()
                total_inserted += 1

                if images and random.random() < 0.35:
                    conn.execute(
                        text("INSERT INTO review_images (review_id, url) VALUES (:r, :u)"),
                        {"r": rid, "u": random.choice(images)},
                    )
            print(f"  activity {aid}: inserted {target} reviews.")

        print(f"\nInserted {total_inserted} reviews total.")

    # Verification summary (read-only).
    with engine.connect() as conn:
        print("\nReviews per Finuo activity:")
        rows = conn.execute(text(
            "SELECT a.id, a.title, count(r.id) AS reviews, ROUND(AVG(r.rating), 2) AS avg_seeded, "
            "       a.average_rating AS shown_avg, a.total_reviews AS shown_total "
            "FROM activities a LEFT JOIN reviews r ON r.activity_id = a.id "
            "WHERE a.vendor_id = :v GROUP BY a.id, a.title, a.average_rating, a.total_reviews "
            "ORDER BY a.id"
        ), {"v": VENDOR_ID}).fetchall()
        for r in rows:
            print(f"  [{r.id}] {r.title[:38]:<38} rows={r.reviews:>2} "
                  f"seeded_avg={r.avg_seeded}  shown={r.shown_avg}/{r.shown_total}")


if __name__ == "__main__":
    main()
