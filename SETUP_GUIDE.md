# FindTravelMate - Terminal Setup Guide

> **Consolidates**: Terminal/local development sections from README.md and previous documentation

This guide provides step-by-step instructions to run the FindTravelMate travel website locally using multiple terminal windows (non-Docker setup).

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (via Docker or local installation)
- npm or yarn

## Overview

The FindTravelMate platform consists of:
- **Backend**: FastAPI application (Python)
- **Frontend**: Next.js application (TypeScript/React)
- **Database**: PostgreSQL

## Terminal Setup (3 Terminal Windows Required)

### Terminal 1: Database Setup

#### Option A: Using Docker (Recommended)
```bash
# Navigate to project root
cd /path/to/site-travel

# Start PostgreSQL container
docker-compose up -d postgres
```

#### Option B: Local PostgreSQL
```bash
# Start PostgreSQL service (if installed locally)
brew services start postgresql
# or
sudo service postgresql start

# Create database
createdb findtravelmate
```

### Terminal 2: Backend Setup

```bash
# Navigate to backend directory
cd /path/to/site-travel/backend

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python init_db.py

# Start backend server with correct environment variables
export DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"
export APP_NAME="FindTravelMate"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### Terminal 3: Frontend Setup

```bash
# Navigate to frontend directory
cd /path/to/site-travel/frontend

# Install dependencies
npm install

# Start frontend with correct API URL
NEXT_PUBLIC_API_URL="http://localhost:8000/api/v1" npm run dev
```

**Frontend will be available at:**
- Website: http://localhost:3000

## Environment Configuration

### Backend Environment Variables (`backend/.env`)
```env
# Application
APP_NAME="FindTravelMate"
APP_VERSION="1.0.0"
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://hongyusu@localhost:5432/findtravelmate
DATABASE_ECHO=False

# Security
SECRET_KEY=your-secret-key-change-this-in-production-make-it-very-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

### Frontend Environment Variables (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Database Initialization

The `init_db.py` script creates:
- Database tables
- Admin user: `admin@findtravelmate.com` / `admin123`
- Customer user: `customer@example.com` / `customer123`
- 5 Vendor accounts: `vendor1-5@example.com` / `vendor123`
- 10 destinations (cities)
- 8 categories
- 25+ sample activities
- Sample reviews and bookings

## Verification Steps

### 1. Database Verification
```bash
# Connect to database
psql postgresql://hongyusu@localhost:5432/findtravelmate

# Check data
SELECT COUNT(*) FROM activities;
SELECT COUNT(*) FROM destinations;
SELECT COUNT(*) FROM categories;
```

### 2. Backend API Verification
```bash
# Test API endpoints
curl http://localhost:8000/api/v1/activities/categories
curl http://localhost:8000/api/v1/activities/destinations
curl http://localhost:8000/api/v1/activities/search?limit=5
```

### 3. Frontend Verification
Visit http://localhost:3000 and verify:
- Homepage loads with data
- Categories and destinations are displayed
- Activities are shown
- Navigation works

## Troubleshooting

### Common Issues

#### 1. "ui has no data" / Frontend shows no data
**Cause**: Environment variable override issue
**Solution**: Start frontend with explicit environment variable:
```bash
NEXT_PUBLIC_API_URL="http://localhost:8000/api/v1" npm run dev
```

#### 2. CORS Errors in Browser Console
**Cause**: Frontend making requests to wrong URL
**Check**: Browser console for XMLHttpRequest errors
**Solution**: Ensure `NEXT_PUBLIC_API_URL` is correctly set

#### 3. Database Connection Errors
**Cause**: PostgreSQL not running or wrong connection string
**Solutions**:
- Check if PostgreSQL is running: `docker-compose ps`
- Verify DATABASE_URL format: `postgresql://user@host:port/database`
- For local PostgreSQL: `postgresql://hongyusu@localhost:5432/findtravelmate`

#### 4. Backend Import Errors
**Cause**: Missing dependencies or wrong Python environment
**Solutions**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version`

#### 5. Frontend Build Errors
**Cause**: Missing dependencies or Node.js version issues
**Solutions**:
- Install dependencies: `npm install`
- Clear cache: `npm run build --clean`
- Check Node.js version: `node --version`

### Port Conflicts

If ports are already in use:
- Backend (8000): Change PORT in `backend/.env`
- Frontend (3000): Use `npm run dev -- -p 3001`
- Database (5432): Update docker-compose.yml

## Development Workflow

### Starting Development Session
1. Open 3 terminal windows
2. Terminal 1: Start database (`docker-compose up -d postgres`)
3. Terminal 2: Start backend (see Backend Setup above)
4. Terminal 3: Start frontend (see Frontend Setup above)
5. Verify all services are running

### Stopping Services
```bash
# Stop frontend: Ctrl+C in Terminal 3
# Stop backend: Ctrl+C in Terminal 2
# Stop database: docker-compose down
```

## Test Accounts

### Admin Account
- Email: `admin@findtravelmate.com`
- Password: `admin123`
- Access: Admin dashboard at http://localhost:3000/admin

### Customer Account
- Email: `customer@example.com`
- Password: `customer123`
- Access: Customer features

### Vendor Accounts
- Email: `vendor1@example.com` to `vendor5@example.com`
- Password: `vendor123`
- Access: Vendor dashboard at http://localhost:3000/vendor

## Project Structure

```
site-travel/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── main.py         # FastAPI app
│   ├── init_db.py          # Database initialization
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── lib/              # Utilities (API client)
│   └── package.json      # Node.js dependencies
└── docker-compose.yml    # Database setup
```

## Next Steps

After successful setup:
1. Explore the API documentation at http://localhost:8000/api/v1/docs
2. Test user registration and login
3. Browse activities and destinations
4. Test booking flow
5. Access admin panel for content management