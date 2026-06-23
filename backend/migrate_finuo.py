#!/usr/bin/env python3
"""Migration for the FinuoTravel rebrand + activity availability tag.

What it does (all idempotent — safe to re-run, and safe to run on every
container start because it never clobbers data that operators later change
through the UI except the one-time availability seeding, which is guarded):

  1. Always: add the ``activities.is_available`` column if it does not exist
     (BOOLEAN NOT NULL DEFAULT TRUE) so the ORM never selects a missing column.
  2. Always: rebrand any leftover ``@findtravelmate.com`` user emails to
     ``@finuo.fi`` (e.g. the admin demo account) so logins match the new brand.
  3. Seed availability ONLY when a Finuo provider vendor exists: set
     ``is_available = TRUE`` for that vendor's activities and ``FALSE`` for all
     others (provider matched by ``company_name ILIKE 'finuo%'`` so it survives
     id changes / restores). If no Finuo vendor is present (e.g. a fresh DB
     restored from the legacy demo backup), availability is left at its default
     (all available) rather than marking the whole catalogue unavailable.

Run inside the backend container:
    docker exec travel_backend python /app/migrate_finuo.py
It is also invoked automatically from docker-entrypoint.sh after first-time
demo-data restore. Both paths are idempotent.
"""

import os
import sys

from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/findtravelmate"
)
FINUO_MATCH = "finuo%"  # ILIKE pattern identifying the Finuo provider vendor(s)

engine = create_engine(DATABASE_URL)


def main() -> None:
    """Apply the schema + data migration and print a verification summary."""
    with engine.begin() as conn:
        # 1. Add the column if missing (idempotent, backfills existing rows to TRUE).
        conn.execute(
            text(
                "ALTER TABLE activities "
                "ADD COLUMN IF NOT EXISTS is_available BOOLEAN NOT NULL DEFAULT TRUE"
            )
        )

        # 2. Rebrand leftover findtravelmate.com user emails.
        email_result = conn.execute(
            text(
                "UPDATE users "
                "SET email = replace(email, '@findtravelmate.com', '@finuo.fi') "
                "WHERE email ILIKE '%@findtravelmate.com'"
            )
        )
        print(f"Rebranded {email_result.rowcount} user email(s) to @finuo.fi.")

        # 3. Seed availability only if a Finuo provider vendor exists.
        finuo_vendors = conn.execute(
            text("SELECT id, company_name FROM vendors WHERE company_name ILIKE :m"),
            {"m": FINUO_MATCH},
        ).fetchall()
        if finuo_vendors:
            print("Finuo provider vendor(s):")
            for v in finuo_vendors:
                print(f"  - id={v.id}  {v.company_name}")
            result = conn.execute(
                text(
                    "UPDATE activities SET is_available = "
                    "(vendor_id IN (SELECT id FROM vendors WHERE company_name ILIKE :m))"
                ),
                {"m": FINUO_MATCH},
            )
            print(f"Seeded availability on {result.rowcount} activities "
                  "(Finuo = available, others = unavailable).")
        else:
            print(f"⚠️  No vendor matching '{FINUO_MATCH}' found — leaving availability "
                  "at default (all available); column added and emails rebranded.")

    # Verification summary (read-only).
    with engine.connect() as conn:
        print("\nAvailability by vendor:")
        rows = conn.execute(
            text(
                "SELECT v.company_name, "
                "       COUNT(*) AS total, "
                "       SUM(CASE WHEN a.is_available THEN 1 ELSE 0 END) AS available "
                "FROM activities a JOIN vendors v ON v.id = a.vendor_id "
                "GROUP BY v.company_name ORDER BY available DESC, v.company_name"
            )
        ).fetchall()
        for r in rows:
            print(f"  {r.company_name:<45} {r.available}/{r.total} available")

        admin = conn.execute(
            text("SELECT email FROM users WHERE CAST(role AS TEXT) ILIKE 'admin' ORDER BY id")
        ).fetchall()
        print("\nAdmin account email(s):")
        for a in admin:
            print(f"  - {a.email}")


if __name__ == "__main__":
    main()
