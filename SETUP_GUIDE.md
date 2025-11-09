# FindTravelMate - Terminal Setup Guide

This guide provides step-by-step instructions to run the FindTravelMate travel website locally using multiple terminal windows. This is the **non-Docker** setup for local development.

> **For Docker setup**, see [DOCKER_SETUP_GUIDE.md](DOCKER_SETUP_GUIDE.md)

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (local installation)
- npm or yarn
- Git

## Overview

The FindTravelMate platform consists of:

- **Backend**: FastAPI application (Python)
- **Frontend**: Next.js application (TypeScript/React)
- **Database**: PostgreSQL

## Terminal Setup (3 Terminal Windows Required)

### Terminal 1: Database Setup

```bash
# Start PostgreSQL service
brew services start postgresql  # macOS
# or
sudo service postgresql start   # Linux

# Create database
createdb findtravelmate

# Verify database creation
psql -l | grep findtravelmate
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

# Set environment variables and start backend server
export DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"
export APP_NAME="FindTravelMate"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:**

- API: <http://localhost:8000>
- Swagger Docs: <http://localhost:8000/api/v1/docs>
- ReDoc: <http://localhost:8000/api/v1/redoc>

### Terminal 3: Frontend Setup

```bash
# Navigate to frontend directory
cd /path/to/site-travel/frontend

# Install dependencies
npm install

# Set API URL and start frontend development server
NEXT_PUBLIC_API_URL="http://localhost:8000/api/v1" npm run dev
```

**Frontend will be available at:**

- Website: <http://localhost:3000>

## Environment Configuration

### Backend Environment Variables (Optional)

Create `backend/.env` for custom configuration:

```env
# Database (adjust username as needed)
DATABASE_URL=postgresql://your_username@localhost:5432/findtravelmate

# Application
APP_NAME="FindTravelMate"
DEBUG=True

# Security (generate secure keys for production)
SECRET_KEY=your-secret-key-change-this-in-production-make-it-very-long-and-random

# CORS (default allows localhost:3000)
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend Environment Variables (Optional)

Create `frontend/.env.local` if you need custom API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

**Note**: Most environment variables have sensible defaults and don't require configuration for local development.

## Database Initialization

The `init_db.py` script automatically creates:

**Database Schema:**

- All required database tables and relationships

**Sample Data:**

- **Users**: Admin, customer, and 5 vendor accounts
- **Destinations**: 10+ cities worldwide
- **Categories**: 8 activity types
- **Activities**: 21+ sample activities with full details
- **Reviews**: Sample reviews with ratings and images
- **Bookings**: Sample booking data

**Test Accounts Created:**

- Admin: `admin@findtravelmate.com` / `admin123`
- Customer: `customer@example.com` / `customer123`
- Vendors: `vendor1-5@example.com` / `vendor123`

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

# Check API documentation
open http://localhost:8000/docs  # macOS
# or visit http://localhost:8000/docs in your browser
```

### 3. Frontend Verification

Visit <http://localhost:3000> and verify:

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

```bash
# Check if PostgreSQL is running
brew services list | grep postgresql  # macOS
# or
sudo service postgresql status        # Linux

# Start PostgreSQL if not running
brew services start postgresql        # macOS
# or
sudo service postgresql start        # Linux

# Verify DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://username@localhost:5432/findtravelmate
```

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

#### 6. Port Conflicts

**Cause**: Ports already in use by other applications
**Solutions**:

```bash
# Check which process is using a port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL

# Kill process using port (if safe to do so)
kill -9 $(lsof -t -i:3000)

# Alternative: Use different ports
# Frontend: npm run dev -- -p 3001
# Backend: Change PORT in backend/.env
```

## Development Workflow

### Starting Development Session

1. Open 3 terminal windows
2. **Terminal 1**: Start PostgreSQL database service
3. **Terminal 2**: Start backend server (see Backend Setup above)
4. **Terminal 3**: Start frontend development server (see Frontend Setup above)
5. Verify all services are running and accessible

### Stopping Services

```bash
# Stop frontend: Ctrl+C in Terminal 3
# Stop backend: Ctrl+C in Terminal 2
# Stop database:
brew services stop postgresql  # macOS
# or
sudo service postgresql stop   # Linux
```

## Test Accounts

### Admin Account

- Email: `admin@findtravelmate.com`
- Password: `admin123`
- Access: Admin dashboard at <http://localhost:3000/admin>

### Customer Account

- Email: `customer@example.com`
- Password: `customer123`
- Access: Customer features

### Vendor Accounts

- Email: `vendor1@example.com` to `vendor5@example.com`
- Password: `vendor123`
- Access: Vendor dashboard at <http://localhost:3000/vendor>

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
└── README.md            # Project documentation
```

## Next Steps

After successful local setup:

1. Explore the API documentation at <http://localhost:8000/api/v1/docs>
2. Test user registration and login flows
3. Browse activities and destinations
4. Test booking functionality
5. Access admin panel for content management
6. Develop and test new features locally
