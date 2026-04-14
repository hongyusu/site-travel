# FindTravelMate

A full-stack travel activities marketplace built with FastAPI and Next.js. Customers browse and book travel experiences, vendors manage activities, and admins moderate the platform.

## Quick Start

```bash
docker compose up -d --build    # Build and start all 5 services
```

Database auto-initializes with 70 activities, 30 categories, 35 destinations, and demo accounts on first startup.

For remote servers, pass the IP so the frontend builds with the correct API URL:
```bash
./deploy.sh 123.45.67.89
```

### Demo Accounts

| Role     | Email                        | Password     |
|----------|------------------------------|--------------|
| Admin    | admin@findtravelmate.com     | admin123     |
| Customer | customer@example.com         | customer123  |
| Vendor   | vendor1@example.com          | vendor123    |

**Access Points:**
- Frontend: http://localhost
- API Docs: http://localhost/docs
- Admin Panel: http://localhost/admin/dashboard

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router), TypeScript 5, Tailwind CSS 3.4 |
| State | Zustand 5, React Hook Form + Zod, Axios |
| Backend | FastAPI 0.104, Python 3.12, SQLAlchemy 2.0, Pydantic v2 |
| Database | PostgreSQL 15, Redis 7 |
| Auth | JWT (access + refresh tokens), bcrypt, role-based access |
| Infra | Docker + Docker Compose, Nginx 1.25 reverse proxy |
| Email | Resend API with Jinja2 templates |

## Features

### Customer
- Advanced search with 15+ filters (price, duration, rating, category, destination, features)
- Activity details with image gallery, video, timeline/itinerary, reviews, similar activities
- Booking with time slot selection, pricing tiers (Standard/Premium/VIP), add-ons
- Session-based shopping cart (works for guests)
- Wishlist, booking history, review submission with images
- Multi-language support (English, Spanish, Chinese, French)
- Currency switching (EUR/CNY)

### Vendor Portal
- Dashboard with revenue, bookings, and activity statistics
- Activity management: create/edit with timeline editor, time slots, multi-tier pricing, add-ons, meeting points, accessibility options
- Booking management: approve, reject, cancel

### Admin Dashboard
- Platform statistics (users, activities, bookings, revenue)
- User and vendor management (toggle status, verify vendors)
- Activity and review moderation

## Architecture

```
Browser  ->  Nginx (:80)  ->  Next.js (:3000)   # Frontend
                           ->  FastAPI (:8000)   # Backend API
                                   |
                              PostgreSQL (:5432)
                              Redis (:6379)
```

## Project Structure

```
site-travel/
├── backend/
│   ├── app/
│   │   ├── api/v1/            # 55 API endpoints across 7 modules
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic validation schemas
│   │   ├── core/security.py   # JWT + password hashing
│   │   ├── services/email.py  # Resend email service
│   │   ├── main.py            # FastAPI app entry point
│   │   └── config.py          # Environment-based configuration
│   ├── backups/               # SQL backup files
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/                   # 40 Next.js pages
│   ├── components/            # 26 React components
│   ├── contexts/              # Language and location contexts
│   ├── lib/api.ts             # Axios API client
│   ├── types/index.ts         # TypeScript interfaces
│   └── Dockerfile
├── nginx/nginx.conf           # Reverse proxy configuration
├── scripts/                   # Verification scripts
├── docker-compose.yml         # All 5 services in one file
├── deploy.sh                  # One-command deploy script
└── backup.sh                  # Database backup
```

## Database

34 tables (including translation tables for 4 languages).

**Demo data:** 30 categories, 35 destinations, 70 activities, 12 vendors, 423 reviews, 210 time slots

Key entities and relationships:
- Users (customer/vendor/admin roles) -> Bookings, Reviews, Cart, Wishlist
- Vendors -> Activities
- Activities -> Images, Timelines, Time Slots, Pricing Tiers, Add-ons, Meeting Points, Highlights, Includes, FAQs
- Reviews -> Images, Category Ratings

## API Endpoints (55 total)

| Module | Endpoints | Key Routes |
|--------|-----------|------------|
| Auth | 6 | register, register-vendor, login, refresh, me, statistics |
| Activities | 12 | search, categories, destinations, CRUD, similar, toggle-status |
| Bookings | 10 | create, my bookings, vendor bookings, cancel, availability |
| Cart | 6 | list, add, update, remove, clear, total |
| Reviews | 6 | list by activity, create, update, delete, helpful, my reviews |
| Wishlist | 4 | list, add, remove, check |
| Admin | 11 | stats, users, vendors, activities, bookings, reviews management |

Full API documentation available at `/api/v1/docs` (Swagger UI).

## Deployment

Single `docker-compose.yml` runs everything. All defaults are built-in — no `.env` configuration required for local demo.

```bash
# Local
docker compose up -d --build

# Remote server (Hetzner, DigitalOcean, any VPS with Docker)
# Pass server IP so frontend builds with correct API URL:
./deploy.sh YOUR_SERVER_IP

# Backup & Restore
docker exec findtravelmate_db pg_dump -U postgres -d findtravelmate \
  --clean --if-exists > backend/backups/backup_$(date +%F).sql

docker exec -i findtravelmate_db psql -U postgres -d findtravelmate \
  < backend/backups/backup_2026-04-14_polished.sql
```

Services: PostgreSQL 15, Redis 7, FastAPI backend, Next.js frontend, Nginx reverse proxy.

For remote deployment, the only thing to override is `NEXT_PUBLIC_API_URL` (baked into frontend at build time). The deploy script handles this automatically when you pass a server IP.

## Internationalization

- **Languages**: English, Spanish, Chinese, French
- **Frontend**: Custom LanguageContext with `getTranslation()` calls
- **Backend**: Translation tables for activities, categories, destinations (10 translation tables)
- **Currency**: EUR (default) with client-side CNY conversion

## Design System

- **Primary color**: #FC6500 (orange)
- **Font**: System font stack
- **Components**: Tailwind CSS utility classes
- **Responsive**: Mobile-first with sm/md/lg/xl breakpoints
- **Icons**: Lucide React

Built with [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/)
