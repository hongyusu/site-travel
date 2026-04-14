# Scripts

## Deployment

```bash
# Deploy everything (from project root)
./deploy.sh                    # localhost
./deploy.sh 123.45.67.89       # remote server
```

## Database

```bash
# Backup
docker exec findtravelmate_db pg_dump -U postgres -d findtravelmate \
  --clean --if-exists > backend/backups/backup_$(date +%F).sql

# Restore
docker exec -i findtravelmate_db psql -U postgres -d findtravelmate \
  < backend/backups/backup_2026-04-14_polished.sql

# Verify
docker exec findtravelmate_db psql -U postgres -d findtravelmate \
  -c "SELECT 'activities', count(*) FROM activities UNION ALL SELECT 'categories', count(*) FROM categories;"
```

## Seed Scripts

These were used to generate the demo data. Not needed for normal operation — the backup file contains everything.

| Script | Purpose |
|--------|---------|
| `backend/seed_expansion.py` | Added categories, destinations, vendors, activities |
| `backend/seed_reviews.py` | Added reviews for all activities |
| `backend/seed_time_slots.py` | Added morning/afternoon/evening time slots |

Run via Docker (requires the app network):
```bash
docker run --rm --network site-travel_app-network \
  -v $(pwd)/backend:/app -w /app \
  -e DATABASE_URL=postgresql://postgres:password@findtravelmate_db:5432/findtravelmate \
  python:3.12-slim bash -c "pip install -q sqlalchemy psycopg2-binary && python <script>.py"
```

## Verification

```bash
python scripts/verify_deployment.py --local
```
