# FinuoTravel

A full-stack travel-activities marketplace (Viator/GetYourGuide-style) built with FastAPI and Next.js. Customers browse and book travel experiences, vendors manage activities, and admins moderate the platform.

**Live:** https://travel.finuo.fi  ·  **API docs:** https://travel.finuo.fi/api/v1/docs

> Also reachable at the raw host `http://178.104.206.21:8083` (no TLS). The HTTPS domain is the canonical URL.

### Demo accounts
| Role     | Email                        | Password     |
|----------|------------------------------|--------------|
| Admin    | admin@finuo.fi     | admin123     |
| Customer | customer@example.com         | customer123  |
| Vendor   | vendor1@example.com          | vendor123    |

> Demo credentials only — rotate before any real production use.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router), TypeScript 5, Tailwind CSS 3.4 |
| State | Zustand, React Hook Form + Zod, Axios |
| Backend | FastAPI 0.104, Python 3.12, SQLAlchemy 2.0, Pydantic v2 |
| Database | PostgreSQL 15, Redis 7 |
| Auth | JWT (access + refresh), bcrypt, role-based access |
| Infra | Docker + Docker Compose, Nginx reverse proxy, Let's Encrypt TLS |
| Email | Resend API with Jinja2 templates |
| Analytics | Google Analytics 4 (`NEXT_PUBLIC_GA_ID`) |

## Features

### Customer
- Search with 15+ filters: price, duration, rating, **category, destination, provider**, features
- **Multilingual search** — matches English, translated content (zh/es/fr), destination & category names, so `桂林` / `Guilin` / `Museums` / `美食` all work
- Activity details: image gallery, video, day-by-day timeline, reviews, similar activities
- Booking with time-slot selection, pricing tiers (Standard/Premium/VIP), add-ons
- Session-based cart (works for guests), wishlist, booking history, reviews with images
- **4 languages** (English / Spanish / Chinese / French) — **defaults to Chinese**
- Currency switching EUR/CNY — **defaults to China/CNY** (display-only client-side conversion)

### Vendor portal
- Dashboard (revenue, bookings, activity stats)
- Activity management: timeline editor, time slots, multi-tier pricing, add-ons, meeting points, accessibility
- Booking management: approve / reject / cancel

### Admin dashboard
- Platform statistics; user/vendor management; activity & review moderation

## Quick Start (local)

```bash
# 1. A SECRET_KEY is REQUIRED (see Security) — create .env first:
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

# 2. Build and start all 5 services
docker compose up -d --build
```
The database auto-initializes (schema + demo data) on first startup.

**Local access:** Frontend `http://localhost` · API docs `http://localhost/docs` · Admin `http://localhost/admin/dashboard`

> ⚠️ `docker compose up` **fails without `SECRET_KEY` in `.env`** (it's no longer a committed default — see Security).

## Architecture

```
Internet ─► host nginx :443 (TLS, travel.finuo.fi) ─► travel stack :8083
                                                          │
   travel_nginx ─► travel_frontend (Next.js :3000)        # UI (API calls are same-origin /api/v1)
                ─► travel_backend  (FastAPI :8000) ─► travel_db (PostgreSQL)
                                                    ─► travel_redis
```
- Containers: `travel_nginx`, `travel_frontend`, `travel_backend`, `travel_db`, `travel_redis`.
- TLS terminates at a **host-level nginx** (Let's Encrypt via certbot, auto-renew) that proxies `travel.finuo.fi` → the travel stack's nginx on `:8083`.
- The frontend calls the API at `window.location.origin/api/v1` (relative) — so it works on any host without a baked API URL.

## Deployment & CD pipeline

**GitHub `main` is the single source of truth.** The server (`/opt/sites/site-travel` on the VPS) is a **pull-only, never-hand-edited checkout**.

```
laptop:  edit ─► git commit ─► git push        # push as the repo owner:
                                                #   git push git@github:hongyusu/site-travel.git main
server:  (deploy = pull + rebuild)
         cd /opt/sites/site-travel
         docker exec travel_db pg_dump -U postgres --clean --if-exists findtravelmate > /root/travel_backup_$(date +%F_%H%M%S).sql
         git fetch origin && git reset --hard origin/main
         docker compose -f docker-compose.yml -f docker-compose.prod.yml build && \
         docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
         curl -sf https://travel.finuo.fi/api/v1/... # verify
```
Notes:
- Build-from-source on the server; the `travel_db` **volume persists across rebuilds** (data is safe; only code/images change).
- Images live in git (`frontend/public/media/`, baked into the frontend image) — no separate asset sync.
- Server is pull-only by design (no push credentials on the box); add new content/images on the laptop and push.
- The repo's legacy `deploy.sh` is **stale** (old `findtravelmate_*` names / port 80) — use the sequence above.

### Backup & restore
```bash
docker exec travel_db pg_dump -U postgres -d findtravelmate --clean --if-exists > backup.sql
docker exec -i travel_db psql -U postgres -d findtravelmate < backup.sql
```
DB dumps are **not** committed to git (gitignored); store them off-box.

## Security

- **`SECRET_KEY`** (JWT signing) is required from `.env` on each host — never committed.
- **CORS** is pinned to the real origins (`travel.finuo.fi`, the raw host, `localhost`); `DEBUG=False` in prod.
- Role-based access; `bcrypt` password hashing; JWT access (30 min) + refresh (7 day) tokens.
- TLS on the public domain (Let's Encrypt, auto-renew).

## Payments (in progress)

Real payments are being built toward a **single-merchant MVP** (platform collects; vendors paid off-platform via `commission_rate`). Status:
- ✅ HTTPS/domain (PCI/Stripe prerequisite) · ✅ security hardening
- ⬜ Alembic migrations → payment data model (`orders`/`payments`/`refunds`/`webhook_events`) → atomic server-side order endpoint + availability locking → frontend checkout rewrite → tests
- ⏸ Stripe wiring (hosted Checkout + webhooks) — deferred until a Stripe account/keys are available

Until then, "checkout" creates bookings **without charging**. See `CLAUDE.md` for the detailed build plan and current state.

## Database

35+ tables (incl. translation tables for 4 languages). **Current data:** ~30 categories, ~37 destinations, ~78 activities, 13 vendors.

Key entities: Users (customer/vendor/admin) → Bookings, Reviews, Cart, Wishlist · Vendors → Activities · Activities → Images, Timelines, Time Slots, Pricing Tiers, Add-ons, Meeting Points, Highlights, Includes, FAQs.

Schema is created via SQLAlchemy `create_all` on an empty DB (Alembic migrations being introduced for payment work — see `CLAUDE.md`). Content is added via idempotent seed scripts in `backend/` (e.g. `seed_china_tours.py`).

## API (`/api/v1`)

| Module | Key routes |
|--------|------------|
| Auth | register, register-vendor, login, refresh, me, statistics |
| Activities | **search** (q / category_slug / destination_slug / **vendor_id** / price / duration / rating / language…), categories, destinations, **providers**, CRUD, similar |
| Bookings | create, my, vendor bookings, cancel, availability |
| Cart | list, add, update, remove, clear, total |
| Reviews | by activity, create, update, delete, helpful, mine |
| Wishlist | list, add, remove, check |
| Admin | stats, users, vendors, activities, bookings, reviews |

Swagger UI at `/api/v1/docs`. Listing responses wrap results as `{ data: [...], pagination: {...} }`. Activity detail is `GET /activities/slug/{slug}` (the bare `/{id}` route expects an integer).

## Internationalization

- **Languages:** English, Spanish, Chinese (default), French — frontend `LanguageContext` + backend `*_translations` tables.
- **Currency:** EUR base, client-side CNY conversion (flat 10×, display-only — never used as a charge amount). Defaults to China/CNY.

## Project Structure

```
site-travel/
├── backend/
│   ├── app/
│   │   ├── api/v1/            # API endpoints (auth, activities, bookings, cart, reviews, wishlist, admin)
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── api/deps.py        # auth dependencies (current user / vendor / admin)
│   │   ├── core/security.py   # JWT + password hashing
│   │   ├── config.py          # env-based settings (SECRET_KEY, CORS, …)
│   │   └── main.py
│   ├── seed_*.py / *_export.json   # idempotent content seeds (incl. China tours, i18n)
│   ├── alembic/               # migrations (being introduced for payments)
│   └── Dockerfile
├── frontend/
│   ├── app/                   # Next.js App Router pages
│   ├── components/            # React components (search/, activities/, booking/, vendor/, layout/)
│   ├── contexts/              # LanguageContext, LocationContext
│   ├── public/media/          # self-hosted images (china/, stock/) — committed to git
│   ├── lib/api.ts             # Axios client
│   └── Dockerfile
├── nginx/nginx.conf
├── scripts/media/             # i18n + media migration helpers
├── docker-compose.yml         # base (5 services)
├── docker-compose.prod.yml    # prod override (container names, NEXT_PUBLIC_* build args)
└── CLAUDE.md                  # detailed internal notes: CD, conventions, payment plan
```

## Design System

- **Primary:** `#FC6500` (orange) · **Icons:** Lucide React · **Styling:** Tailwind, mobile-first.

---
Built with [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/). Deep operational notes live in `CLAUDE.md`.
