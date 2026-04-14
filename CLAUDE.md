# FindTravelMate

## Overview

Full-stack travel activities marketplace (like Viator/GetYourGuide). Three user roles: customers browse/book travel experiences, vendors manage activities, admins moderate the platform.

## Tech Stack

### Backend
- **Python 3.12** with **FastAPI 0.104** + Uvicorn
- **PostgreSQL 15** via SQLAlchemy 2.0 (ORM) + Alembic (migrations)
- **Redis 7** (optional caching)
- **Auth**: JWT (python-jose) + bcrypt. Access tokens: 30min, refresh: 7 days
- **Validation**: Pydantic v2 + pydantic-settings
- **Email**: Resend API with Jinja2 templates (testing mode: redirects to verified email)
- **Dependencies**: `pip install -r requirements.txt` (not Poetry)
- **Code style**: black + flake8 (not ruff/mypy)

### Frontend
- **Next.js 14.2** (App Router) + **TypeScript 5** (strict mode)
- **Styling**: Tailwind CSS 3.4
- **State**: Zustand 5 (global), React Hook Form 7 + Zod 4 (forms), TanStack React Query 5 (installed but mostly unused — pages use direct axios calls in useEffect)
- **HTTP**: Axios with interceptors (auto token refresh, session ID, language params)
- **i18n**: Custom LanguageContext (en, es, zh, fr) — not next-intl
- **Currency**: LocationContext (EU/EUR, CN/CNY with client-side conversion)
- **UI**: Lucide React icons, Embla Carousel, react-hot-toast
- **Build**: `output: 'standalone'` for Docker; ESLint/TS errors ignored during build

### Infrastructure
- **Docker** + Docker Compose with multi-stage builds (single `docker-compose.yml`)
- **Nginx 1.25** reverse proxy (`/` -> frontend:3000, `/api` -> backend:8000)
- **Deploy**: Single `docker compose up -d --build` on any Linux VPS with Docker

## Project Structure

```
site-travel/
├── backend/
│   ├── app/
│   │   ├── api/v1/            # auth(6), activities(12), bookings(10), cart(6), reviews(6), wishlist(4), admin(11) = 55 endpoints
│   │   ├── models/            # SQLAlchemy models → 34 tables (including translations)
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── core/security.py   # JWT + password hashing
│   │   ├── services/email.py  # Resend email integration
│   │   ├── utils/translation.py
│   │   ├── templates/emails/  # Jinja2 email templates
│   │   ├── main.py            # FastAPI app with lifespan (calls init_db on startup)
│   │   ├── config.py          # pydantic-settings based config
│   │   └── database.py        # SQLAlchemy engine + session + Base
│   ├── alembic/               # Database migrations
│   ├── backups/               # SQL backup files
│   ├── initialize_database.py # Restore DB from backup file
│   ├── seed_expansion.py      # Add more categories/activities (run via Docker)
│   ├── requirements.txt       # 39 Python dependencies
│   ├── docker-entrypoint.sh   # Waits for PG, auto-inits DB if AUTO_INIT_DB=true
│   ├── Dockerfile             # Multi-stage (base → deps → dev/prod)
│   └── Dockerfile.dev         # Dev with debugpy + hot reload
├── frontend/
│   ├── app/                   # 40 pages (Next.js App Router)
│   ├── components/            # 26 React components
│   ├── contexts/              # LanguageContext.tsx, LocationContext.tsx
│   ├── lib/api.ts             # Axios API client (env-aware: browser vs SSR Docker)
│   ├── lib/utils.ts           # formatPrice, formatDate, etc.
│   ├── types/index.ts         # All TypeScript interfaces
│   ├── next.config.mjs        # standalone output, remote image patterns
│   ├── tailwind.config.ts     # Custom theme (primary: #FC6500)
│   ├── Dockerfile             # Multi-stage production build
│   └── Dockerfile.dev         # Dev with hot reload
├── nginx/
│   └── nginx.conf             # Reverse proxy config (routes, security headers)
├── scripts/
│   ├── verify_deployment.py   # Deployment verification
│   └── README.md
├── docker-compose.yml         # Single compose: 5 services (pg, redis, backend, frontend, nginx)
├── deploy.sh                  # One-command deploy: ./deploy.sh [server-ip]
├── backup.sh                  # Database backup
└── .env                       # Overrides only (defaults are in docker-compose.yml)
```

## Key Commands

```bash
# Deploy everything (localhost)
docker compose up -d --build
# Or use the deploy script:
./deploy.sh                    # localhost
./deploy.sh 123.45.67.89       # remote server (sets API URL)

# Restore demo data (after first deploy, DB is empty)
docker exec -i findtravelmate_db psql -U postgres -d findtravelmate \
  < backend/backups/backup_2026-04-14_expanded.sql

# Backup
docker exec findtravelmate_db pg_dump -U postgres -d findtravelmate \
  --clean --if-exists > backend/backups/backup_$(date +%F).sql

# Local development (without Docker for frontend/backend)
docker compose up -d postgres redis    # Start DB + Redis only
cd backend && DATABASE_URL=postgresql://postgres:postgres@localhost:5432/findtravelmate \
  uvicorn app.main:app --reload        # Backend on :8000
cd frontend && npm run dev             # Frontend on :3000

# Logs
docker compose logs -f backend         # Follow backend logs
docker compose logs                    # All service logs
```

## Database

34 tables total (including 10 translation tables for en/es/zh/fr).

**Current data:** 30 categories, 35 destinations, 70 activities, 12 vendors, 28 users.

Key entities: users, vendors, activities (with images, timelines, time_slots, pricing_tiers, add_ons, meeting_points, highlights, includes, faqs), bookings, reviews, cart_items, wishlist.

Roles: `CUSTOMER`, `VENDOR`, `ADMIN`. Booking statuses: `PENDING`, `PENDING_VENDOR_APPROVAL`, `CONFIRMED`, `REJECTED`, `CANCELLED`, `COMPLETED`.

**No `init_db.py` seed script exists** — the docker-entrypoint.sh references it but the file is missing. Database is populated via SQL backup restore only. Latest backup: `backend/backups/backup_2026-04-14_expanded.sql`.

## Demo Accounts

| Role     | Email                        | Password     |
|----------|------------------------------|--------------|
| Admin    | admin@findtravelmate.com     | admin123     |
| Customer | customer@example.com         | customer123  |
| Vendor   | vendor1@example.com          | vendor123    |

## API

- **Base**: `/api/v1` — **Docs**: `/api/v1/docs` (Swagger)
- **55 endpoints** across 7 modules
- **Auth**: Bearer token in `Authorization` header
- **Guest cart**: `X-Session-ID` header (persisted in localStorage)
- **Language**: `?language=en|es|zh|fr` query param on content endpoints

## Environment Variables

Required in `.env`:
- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — JWT signing key (32+ chars)
- `ALGORITHM` — JWT algorithm (default: HS256)
- `NEXT_PUBLIC_API_URL` — Frontend API base URL (baked at build time)
- `POSTGRES_PASSWORD` — For Docker PostgreSQL
- `CORS_ORIGINS` — Comma-separated allowed origins
- `RESEND_API_KEY` — For email (optional, logs to console without it)

## Conventions

- Backend routes versioned under `/api/v1/`
- Frontend uses `'use client'` for interactive components
- API client in `frontend/lib/api.ts` — environment-aware (browser: localhost, SSR: Docker hostname)
- Pages fetch data via `useEffect` + axios (not React Query hooks despite dependency)
- Activity lookup is slug-based for SEO-friendly URLs
- Cart is session-based (works for unauthenticated guests)
- Prices in EUR, client-side CNY conversion via LocationContext
- Images use picsum.photos seeded URLs (deterministic based on slug)
- Translation tables follow pattern: `{entity}_translations` with `language` + `{entity}_id` columns

## Deployment

Single `docker-compose.yml` runs all 5 services. No dev/prod split.

```bash
./deploy.sh                    # localhost
./deploy.sh 123.45.67.89       # remote (passes NEXT_PUBLIC_API_URL as build arg)
```

The deploy script `export`s `NEXT_PUBLIC_API_URL` which docker-compose.yml reads via `${NEXT_PUBLIC_API_URL:-http://localhost/api}`. This is baked into the Next.js build at image creation time — changing it requires a rebuild.

Nginx `/health` endpoint proxies to backend `/health` for real health checking.

## Known Limitations

- Local PostgreSQL on macOS shadows Docker port 5432 — run scripts inside Docker or use `docker exec`
- Some activities (IDs 8-22) have generic timeline steps instead of activity-specific ones
- No translations seeded for the 49 expanded activities — only English content
- No HTTPS/SSL — acceptable for demo, add Let's Encrypt for production
- Pre-existing TypeScript errors (ignored by build via `ignoreBuildErrors: true`)
