#!/usr/bin/env python3
"""Add Spanish & French destination-name translations (idempotent).

The DB only had Chinese (zh) rows in destination_translations, so es/fr
destination names fell back to English on the /destinations page. This inserts
es and fr `name` rows for every destination. Names that are identical across
languages (proper nouns) just reuse the English name.

Run inside the backend container:
    docker exec travel_backend python /app/seed_destination_translations_es_fr.py
Idempotent: ON CONFLICT (destination_id, language) DO NOTHING.
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate"
)
engine = create_engine(DATABASE_URL)

# Only names that differ from English are listed; anything missing reuses the
# English name (most city names are identical proper nouns).
ES = {
    "Sydney": "Sídney", "Vienna": "Viena", "Beijing": "Pekín", "Chengdu": "Chengdú",
    "Shanghai": "Shanghái", "Havana": "La Habana", "Prague": "Praga",
    "Copenhagen": "Copenhague", "France · Italy · Switzerland": "Francia · Italia · Suiza",
    "France": "Francia", "Paris": "París", "Iceland": "Islandia", "Reykjavik": "Reikiavik",
    "Italy": "Italia", "Rome": "Roma", "Kyoto": "Kioto", "Tokyo": "Tokio",
    "Norway & the Fjords": "Noruega y los fiordos", "Lisbon": "Lisboa",
    "Cape Town": "Ciudad del Cabo", "Spain & Portugal": "España y Portugal",
    "Stockholm": "Estocolmo", "Switzerland & the Alps": "Suiza y los Alpes",
    "Istanbul": "Estambul", "Dubai": "Dubái", "London": "Londres", "New York": "Nueva York",
}
FR = {
    "Vienna": "Vienne", "Beijing": "Pékin", "Havana": "La Havane",
    "Copenhagen": "Copenhague", "France · Italy · Switzerland": "France · Italie · Suisse",
    "Iceland": "Islande", "Italy": "Italie", "Norway & the Fjords": "La Norvège et les fjords",
    "Lisbon": "Lisbonne", "Cape Town": "Le Cap", "Spain & Portugal": "Espagne et Portugal",
    "Switzerland & the Alps": "La Suisse et les Alpes", "Dubai": "Dubaï",
    "London": "Londres", "Barcelona": "Barcelone",
}


def main():
    with engine.begin() as conn:
        conn.execute(text(
            "SELECT setval(pg_get_serial_sequence('destination_translations','id'),"
            "COALESCE((SELECT MAX(id) FROM destination_translations),0)+1,false)"))
        rows = conn.execute(text("SELECT id, name FROM destinations")).fetchall()
        inserted = {"es": 0, "fr": 0}
        for lang, mapping in (("es", ES), ("fr", FR)):
            for d in rows:
                name = mapping.get(d.name, d.name)
                r = conn.execute(text(
                    "INSERT INTO destination_translations (destination_id, language, name) "
                    "VALUES (:d,:l,:n) ON CONFLICT (destination_id, language) DO NOTHING "
                    "RETURNING id"), {"d": d.id, "l": lang, "n": name}).first()
                if r:
                    inserted[lang] += 1
        print(f"Inserted es={inserted['es']} fr={inserted['fr']} destination name rows "
              f"(of {len(rows)} destinations each).")

    with engine.connect() as conn:
        for lang in ("en", "zh", "es", "fr"):
            cnt = conn.execute(text("SELECT count(*) FROM destination_translations WHERE language=:l"),
                               {"l": lang}).scalar()
            print(f"  {lang}: {cnt} rows")


if __name__ == "__main__":
    main()
