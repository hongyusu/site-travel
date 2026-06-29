#!/usr/bin/env python3
"""Add 5-15 customer reviews to every active activity that currently has none.

Idempotent: activities that already have at least one review are skipped, so
this is safe to re-run. Reviews are multilingual (English-dominant, with some
Chinese/Spanish/French) with realistic weighted ratings, varied dates and
helpful counts, ~30% carrying a photo from the activity's own gallery. Each
touched activity's average_rating / total_reviews is recomputed from its
reviews afterwards.

Run inside the backend container:
    docker exec travel_backend python /app/seed_missing_reviews.py
"""

import os
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, text

random.seed(20260629)
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate"
)
engine = create_engine(DATABASE_URL)

PW_HASH = "$2b$12$TxjAN.QLj4nory7k.VFcF.SSwEEM8e1bPYaVVf0vgMQ3QpI.YM0Cy"
BASE_DATE = datetime(2026, 6, 15, tzinfo=timezone.utc)
HELPFUL = [0, 0, 0, 1, 1, 2, 2, 3, 4, 5, 6, 8, 10, 12, 15, 19, 24, 31]

# Reviewer name pools per language (name, email-local).
USERS = {
    "en": [
        ("Sarah Thompson", "sarah.t"), ("James Wilson", "james.w"),
        ("Emma Becker", "emma.b"), ("David Kim", "david.k"),
        ("Olivia Brown", "olivia.b"), ("Daniel Lee", "daniel.l"),
        ("Hannah Schmidt", "hannah.s"), ("Thomas Anderson", "thomas.a"),
        ("Yuki Tanaka", "yuki.t"), ("Min-jun Park", "minjun.p"),
        ("Laura Mitchell", "laura.m"), ("Niklas Berg", "niklas.b"),
        ("Aisha Khan", "aisha.k"), ("Liam O'Connor", "liam.o"),
        ("Grace Miller", "grace.m"), ("Ethan Clark", "ethan.c"),
        ("Priya Nair", "priya.n"), ("Noah Williams", "noah.w"),
    ],
    "zh": [
        ("王芳", "wangfang"), ("李娜", "lina"), ("张伟", "zhangwei"),
        ("刘洋", "liuyang"), ("陈静", "chenjing"), ("林峰", "linfeng"),
        ("黄蕾", "huanglei"), ("徐明", "xuming"),
    ],
    "es": [
        ("Carlos Gómez", "carlos.g"), ("Lucía Fernández", "lucia.f"),
        ("Javier Ruiz", "javier.r"), ("Marta Sánchez", "marta.s"),
        ("Diego Torres", "diego.t"), ("Elena Navarro", "elena.n"),
    ],
    "fr": [
        ("Chloé Moreau", "chloe.m"), ("Antoine Dubois", "antoine.d"),
        ("Camille Laurent", "camille.l"), ("Hugo Lefevre", "hugo.l"),
        ("Léa Girard", "lea.g"), ("Maxime Rousseau", "maxime.r"),
    ],
}

# (language, title, comment) — generic enough to fit any tour / activity type.
REVIEWS = [
    ("en", "An unforgettable experience", "Beautifully organised from start to finish. Our guide was friendly and full of local knowledge, and every detail was taken care of. Highly recommend!"),
    ("en", "Exceeded our expectations", "We weren't sure what to expect but this was the highlight of our trip. Smooth, well-paced and genuinely fun the whole way through."),
    ("en", "Our guide made the day", "Passionate, patient and so knowledgeable. They brought the place to life with great stories and made sure everyone felt looked after."),
    ("en", "Great value for money", "Honestly better than we expected for the price. No rushing, no hidden costs, just a great experience. Would book again without hesitation."),
    ("en", "Perfectly paced", "Never felt rushed and never felt like we were waiting around. Saw all the highlights and still had a little free time. Thoughtfully planned."),
    ("en", "Fantastic for families", "Travelled with two kids and they loved every minute. The guide was wonderful with them and kept everyone engaged. Stress-free for the parents too."),
    ("en", "A real local insight", "Felt like we saw the authentic side rather than just the tourist spots. The little recommendations along the way were the best part."),
    ("en", "Smooth and well run", "Everything was organised and on time. Easy to find the meeting point, clear communication beforehand, and a great atmosphere throughout."),
    ("en", "Highlight of our holiday", "Out of everything we did on this trip, this stood out. Beautiful, well-guided and full of memories we'll keep for a long time."),
    ("en", "Would absolutely recommend", "From booking to the final goodbye it was seamless and professional. Already told friends back home they have to do this."),
    ("en", "Better than the photos", "It looked good online but was even better in person. Great pacing, lovely group size and a guide who clearly loves what they do."),
    ("en", "Lovely small group", "Not a huge crowd, which made it feel personal. We could ask questions and actually hear the guide. Much nicer than the big bus tours."),
    ("en", "Worth every penny", "Such good value. We learned a lot, had plenty of photo stops and never felt pushed into anything. Genuinely enjoyable."),
    ("en", "Brilliant from start to finish", "Punctual, professional and great fun. The guide had a real sense of humour and made the whole group feel welcome."),
    ("en", "A wonderful afternoon", "Relaxed, informative and beautiful. Exactly the kind of experience we were hoping for. Came away wishing we'd booked a second one."),
    ("en", "Memories to last a lifetime", "A really special experience. Every part was thoughtfully done and the guide went above and beyond to make it memorable."),
    ("en", "So glad we booked this", "Almost skipped it and I'm so glad we didn't. Easily one of the best things we did. Clear, fun and beautifully run."),
    ("en", "Knowledgeable and warm guide", "You can tell when someone genuinely cares. Great stories, great pace, and happy to take extra photos for us. Five stars."),
    ("en", "Easy, fun and memorable", "Booking was simple, the meeting point was easy to find, and the experience itself was a joy. Highly recommend to anyone visiting."),
    ("en", "Great experience overall", "Really enjoyed it. A couple of moments felt a touch quick but the guide was excellent and the highlights more than made up for it."),
    ("en", "Top-notch organisation", "Everything ran like clockwork. Friendly staff, comfortable pace and stunning sights. Would happily do it all again."),
    ("en", "Highly recommended", "A wonderful way to spend a few hours. The guide was engaging and the whole thing was very well put together."),
    ("zh", "非常棒的体验", "从头到尾安排得井井有条，导游热情又专业，讲解生动有趣，每个细节都照顾到了，强烈推荐！"),
    ("zh", "超出预期", "本来没抱太大期待，结果成了这次旅行的亮点，节奏舒适，全程都很愉快。"),
    ("zh", "导游很用心", "导游知识渊博又很有耐心，把当地的故事讲得活灵活现，照顾到每一位游客，体验非常好。"),
    ("zh", "性价比很高", "价格实惠体验却一点不打折，没有强制消费，玩得很放松，下次还想再参加。"),
    ("zh", "全家都很满意", "带着老人和孩子一起，节奏适中大家都跟得上，导游照顾得很周到，是一次轻松愉快的出行。"),
    ("zh", "值得推荐", "预订到结束都很顺畅，沟通及时，氛围轻松，已经推荐给身边的朋友了。"),
    ("zh", "拍照拍到手软", "每个景点导游都知道最佳机位，风景太美了，回来相册都装不下，难忘的一天。"),
    ("zh", "小团体验很自在", "人不多，可以随时提问，比大巴团舒服太多，导游专业又亲切。"),
    ("es", "Una experiencia inolvidable", "Todo perfectamente organizado de principio a fin. El guía fue muy amable y con muchísimo conocimiento local. ¡Muy recomendable!"),
    ("es", "Superó nuestras expectativas", "No sabíamos qué esperar y resultó ser lo mejor del viaje. Ameno, bien organizado y divertido en todo momento."),
    ("es", "El guía hizo el día", "Apasionado, paciente y con mucho conocimiento. Nos cuidó a todos y nos contó historias estupendas. Cinco estrellas."),
    ("es", "Excelente relación calidad-precio", "Mejor de lo que esperábamos por el precio. Sin prisas y sin costes ocultos. Repetiríamos sin dudarlo."),
    ("es", "Perfecto para familias", "Viajamos con niños y se lo pasaron en grande. El guía fue maravilloso con ellos. Sin estrés para los padres."),
    ("es", "Muy recomendable", "Desde la reserva hasta el final, todo impecable y profesional. Una de las mejores cosas que hicimos en el viaje."),
    ("fr", "Une expérience inoubliable", "Parfaitement organisé du début à la fin. Notre guide était chaleureux et très cultivé. Je recommande vivement !"),
    ("fr", "Au-delà de nos attentes", "Nous ne savions pas à quoi nous attendre et ce fut le point fort du voyage. Fluide, bien rythmé et vraiment agréable."),
    ("fr", "Le guide a fait la différence", "Passionné, patient et incollable sur la région. Il a pris soin de tout le monde et raconté de belles anecdotes."),
    ("fr", "Excellent rapport qualité-prix", "Bien mieux que prévu pour le prix. Aucun frais caché, aucun moment d'ennui. Nous recommanderions sans hésiter."),
    ("fr", "Parfait en famille", "Voyagé avec des enfants qui ont adoré. Le guide était formidable avec eux et tout était sans stress pour les parents."),
    ("fr", "Vivement recommandé", "De la réservation à la fin, tout était fluide et professionnel. L'une des meilleures activités de notre séjour."),
]


def ensure_users(conn):
    """Create reviewer users (idempotent) and return {lang: [user_id, ...]}."""
    ids = {}
    for lang, people in USERS.items():
        ids[lang] = []
        for name, local in people:
            email = f"{local}@reviewers.finuo.fi"
            row = conn.execute(text("SELECT id FROM users WHERE email=:e"), {"e": email}).first()
            if row:
                ids[lang].append(row[0])
            else:
                ids[lang].append(conn.execute(
                    text("INSERT INTO users (email,password_hash,full_name,role,email_verified,is_active) "
                         "VALUES (:e,:p,:n,'CUSTOMER',true,true) RETURNING id"),
                    {"e": email, "p": PW_HASH, "n": name}).scalar())
    return ids


def main():
    with engine.begin() as conn:
        # Keep id sequences ahead of any manually inserted rows.
        for tbl in ("users", "reviews", "review_images"):
            conn.execute(text(f"SELECT setval(pg_get_serial_sequence('{tbl}','id'),"
                              f"COALESCE((SELECT MAX(id) FROM {tbl}),0)+1,false)"))

        user_ids = ensure_users(conn)

        acts = conn.execute(text(
            "SELECT a.id, a.vendor_id FROM activities a "
            "WHERE a.is_active = true "
            "AND NOT EXISTS (SELECT 1 FROM reviews r WHERE r.activity_id = a.id) "
            "ORDER BY a.id")).fetchall()

        touched, total = [], 0
        for a in acts:
            imgs = [r[0] for r in conn.execute(
                text("SELECT url FROM activity_images WHERE activity_id=:a"), {"a": a.id}).fetchall()]
            n = random.randint(5, 15)
            picks = random.sample(REVIEWS, min(n, len(REVIEWS)))
            # Distinct reviewers per language within this activity.
            pool = {lang: random.sample(uids, len(uids)) for lang, uids in user_ids.items()}
            for lang, title, comment in picks:
                uid = pool[lang].pop() if pool[lang] else random.choice(user_ids[lang])
                rating = random.choices([5, 4, 3, 2], weights=[60, 28, 9, 3])[0]
                created = BASE_DATE - timedelta(
                    days=random.randint(5, 430), hours=random.randint(0, 23), minutes=random.randint(0, 59))
                rid = conn.execute(text(
                    "INSERT INTO reviews (user_id,activity_id,vendor_id,rating,title,comment,"
                    "is_verified_booking,helpful_count,created_at) "
                    "VALUES (:u,:a,:v,:r,:t,:c,:vb,:h,:ts) RETURNING id"),
                    {"u": uid, "a": a.id, "v": a.vendor_id, "r": rating, "t": title, "c": comment,
                     "vb": random.random() < 0.85, "h": random.choice(HELPFUL), "ts": created}).scalar()
                if imgs and random.random() < 0.30:
                    conn.execute(text("INSERT INTO review_images (review_id,url) VALUES (:r,:u)"),
                                 {"r": rid, "u": random.choice(imgs)})
                total += 1
            touched.append(a.id)

        if touched:
            conn.execute(text(
                "UPDATE activities a SET total_reviews=s.cnt, average_rating=s.avg FROM "
                "(SELECT activity_id, COUNT(*) cnt, ROUND(AVG(rating)::numeric,1) avg "
                " FROM reviews GROUP BY activity_id) s "
                "WHERE a.id=s.activity_id AND a.id = ANY(:ids)"), {"ids": touched})

        print(f"Inserted {total} reviews across {len(touched)} activities that had none.")

    with engine.connect() as conn:
        remaining = conn.execute(text(
            "SELECT count(*) FROM activities a WHERE a.is_active "
            "AND NOT EXISTS (SELECT 1 FROM reviews r WHERE r.activity_id=a.id)")).scalar()
        print(f"Active activities still without reviews: {remaining}")


if __name__ == "__main__":
    main()
