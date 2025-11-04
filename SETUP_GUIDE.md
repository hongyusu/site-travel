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

## Production AWS Deployment

### AWS Server Information
- **Server**: `ssh -i "ocrbot.pem" ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com`
- **Frontend URL**: http://54.217.173.125:3000
- **Backend API**: http://54.217.173.125:8000/api/v1
- **API Documentation**: http://54.217.173.125:8000/api/v1/docs

### Services Configuration
- **Backend**: Systemd service (`findtravelmate-backend.service`)
- **Frontend**: PM2 process manager
- **Database**: PostgreSQL system service

### Service Management Commands
```bash
# Backend service
sudo systemctl status findtravelmate-backend
sudo systemctl restart findtravelmate-backend
sudo systemctl stop findtravelmate-backend

# Frontend service  
pm2 list
pm2 restart findtravelmate-frontend
pm2 stop findtravelmate-frontend
pm2 logs findtravelmate-frontend

# Database service
sudo systemctl status postgresql
```

### Demo Accounts (AWS Production)
- **Customer**: `customer@example.com / customer123` ✅ Tested working
- **Admin**: `admin@findtravelmate.com / admin123` 
- **Vendor**: `vendor1@example.com / vendor123` (vendor1-5 available)

## AWS Database Management

### Database Backup and Restoration Process

#### Creating Local Database Backup
```bash
# From project root directory
cd /path/to/site-travel

# Ensure DATABASE_URL is set for local database
export DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"

# Create backup using the provided script
python backend/backup_database.py
# Output: backup_YYYY-MM-DD_HH-MM-SS.sql (e.g., backup_2025-11-04_22-45-58.sql)
```

#### Transferring Backup to AWS
```bash
# Copy backup file to AWS server
scp -i "ocrbot.pem" backup_2025-11-04_22-45-58.sql ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com:/home/ubuntu/
```

#### Restoring Database on AWS
```bash
# SSH into AWS server
ssh -i "ocrbot.pem" ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com

# Set database password (if needed)
export PGPASSWORD=ubuntu123

# Drop existing database (DESTRUCTIVE - be careful!)
dropdb --host localhost --port 5432 --username ubuntu --if-exists findtravelmate

# Create fresh database
createdb --host localhost --port 5432 --username ubuntu findtravelmate

# Restore from backup
psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate --file backup_2025-11-04_22-45-58.sql --quiet

# Verify restoration
psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate --command "SELECT COUNT(*) FROM activities;"
psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate --command "SELECT name FROM categories ORDER BY name;"
```

#### Database User Setup (Required for Backend Service)
```bash
# Connect to PostgreSQL as superuser
sudo -u postgres psql

# Create ubuntu user with password (if doesn't exist)
CREATE USER ubuntu WITH PASSWORD 'ubuntu123';
GRANT ALL PRIVILEGES ON DATABASE findtravelmate TO ubuntu;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ubuntu;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ubuntu;
\q
```

### Data Consistency Verification

#### Comparing Local vs AWS Database
```bash
# Local database check
export DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM activities;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM categories;"
psql $DATABASE_URL -c "SELECT name FROM categories ORDER BY name;"

# AWS database check (via SSH)
ssh -i "ocrbot.pem" ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com "
export PGPASSWORD=ubuntu123
psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate -c 'SELECT COUNT(*) FROM activities;'
psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate -c 'SELECT COUNT(*) FROM categories;'
psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate -c 'SELECT name FROM categories ORDER BY name;'
"
```

#### Expected Data After Restoration (November 2025)
- **Categories**: 10 (Tours, Food & Drink, Museums & Culture, Outdoor Activities, Study Tours, Adventure, Luxury Experiences, Family-Friendly, Historical Sites, Nature & Wildlife)
- **Activities**: 21 (including Stockholm tours, Louvre visits, Chinese cultural experiences)
- **Destinations**: 10+ cities worldwide
- **Users**: 20+ (admin, customers, vendors)

## AWS Deployment Issues and Solutions

### Issue 1: CSS Not Loading (FIXED ✅)
**Problem**: CSS files returning 404, website appeared unstyled
**Root Cause**: 
- Multiple conflicting Next.js processes running on port 3000
- PM2 configuration issues with production vs development mode
**Solution**:
```bash
# Kill conflicting processes
ps aux | grep -E '(node|next|npm)' | grep -v grep
kill [process_ids]

# Use development mode for AWS (simpler and more reliable)
# ecosystem.config.js:
{
  script: 'npm',
  args: 'run dev',
  env: {
    NODE_ENV: 'development',
    NEXT_PUBLIC_API_URL: 'http://54.217.173.125:8000/api/v1'
  }
}
```

### Issue 2: Database Data Inconsistency (FIXED ✅)
**Problem**: AWS database had different/outdated data compared to local development
**Root Cause**: 
- AWS database was initialized with older sample data
- Local database had been updated with new categories and activities
- No automated sync between local and production databases
**Solution**:
```bash
# Complete database replacement workflow:
# 1. Create fresh backup from local database
# 2. Transfer backup to AWS server  
# 3. Drop and recreate AWS database
# 4. Restore from local backup
# 5. Verify data consistency

# Key Learning: Always verify data consistency between environments
```

### Issue 3: Backend Service Configuration (FIXED ✅)
**Problem**: Backend API service failing to start due to configuration errors
**Root Cause**: 
- CORS_ORIGINS environment variable format causing parsing errors
- Pydantic settings validation failing
- Database authentication issues (missing password)
**Solution**:
```bash
# Fixed systemd service configuration
# /etc/systemd/system/findtravelmate-backend.service:
[Service]
Environment=DATABASE_URL=postgresql://ubuntu:ubuntu123@localhost:5432/findtravelmate
Environment=APP_NAME=FindTravelMate
Environment=SECRET_KEY=fc63a21a723d1c5cd0da733b3fcb84f5db481cf61439270181aba7c65809e53f
# Note: Removed CORS_ORIGINS to use defaults from config.py

sudo systemctl daemon-reload && sudo systemctl restart findtravelmate-backend
```

### Issue 4: Frontend Restart Loops (FIXED ✅)
**Problem**: PM2 frontend service constantly restarting (900+ restarts)
**Root Cause**: 
- Port 3000 conflicts from orphaned Next.js processes
- PM2 trying to start multiple instances on same port
**Solution**:
```bash
# Clean shutdown and restart
pm2 stop findtravelmate-frontend && pm2 delete findtravelmate-frontend
sudo kill $(sudo ss -tulpn | grep :3000 | awk '{print $7}' | cut -d',' -f2 | cut -d'=' -f2)
pm2 start ecosystem.config.js
```

### Working Configuration (November 2025)
- **Frontend**: Next.js development mode via PM2
- **Backend**: Systemd service with simplified configuration (no CORS_ORIGINS override)
- **Database**: PostgreSQL system service with complete data restoration from local
- **Static Assets**: Served correctly by Next.js dev server
- **API Connectivity**: Full backend functionality verified
- **Data Sync**: Complete consistency between local and AWS environments

## Deployment Best Practices & Lessons Learned

### Database Management Lessons

#### 1. Environment Data Consistency
**Problem**: Production and development databases can diverge over time
**Solution**: 
- Implement regular database sync procedures
- Always verify data consistency before and after deployments
- Use explicit backup/restore workflows for critical updates

#### 2. Database Authentication
**Problem**: Default PostgreSQL setup may not have proper user credentials
**Solution**:
- Create dedicated database users with passwords for application access
- Set proper permissions for all tables, sequences, and schemas
- Document database credentials securely

#### 3. Backup Strategy
**Lessons Learned**:
- Create timestamped backups: `backup_YYYY-MM-DD_HH-MM-SS.sql`
- Verify backup integrity before restoration
- Use `--quiet` flag for production restores to reduce log noise
- Always test restoration process in non-production environment first

### Service Configuration Lessons

#### 1. Environment Variable Management
**Problem**: Complex environment variables (like JSON arrays) can cause parsing errors
**Solution**:
- Use application defaults when possible instead of environment overrides
- Keep systemd service files simple and minimal
- Document working configurations for future reference

#### 2. Process Management
**Problem**: Multiple processes competing for same ports cause instability
**Solution**:
- Always clean up orphaned processes before restarting services
- Use process managers (PM2, systemd) consistently
- Monitor restart counters to detect configuration issues early

#### 3. Development vs Production Mode
**Key Finding**: For AWS deployment, Next.js development mode proved more reliable than production build
**Reasons**:
- Simpler asset serving
- Better error reporting
- Easier debugging
- No build step complexity

### Troubleshooting Methodology

#### 1. Layer-by-Layer Debugging
1. **Database Layer**: Verify data and connectivity first
2. **Backend Layer**: Test API endpoints independently
3. **Frontend Layer**: Check static assets and API integration
4. **Service Layer**: Ensure all processes are running correctly

#### 2. Verification Commands
```bash
# Service status checks
sudo systemctl status findtravelmate-backend
pm2 status

# Database connectivity
psql $DATABASE_URL -c "SELECT COUNT(*) FROM activities;"

# API endpoint testing
curl -s http://localhost:8000/api/v1/activities/categories

# Port conflict detection
sudo ss -tulpn | grep :3000
sudo ss -tulpn | grep :8000
```

#### 3. Log Analysis Priority
1. **systemctl/journalctl logs**: For service startup issues
2. **PM2 logs**: For frontend application errors
3. **Database logs**: For connection and query issues
4. **Browser console**: For client-side API issues

### Future Deployment Considerations

#### 1. Automated Database Sync
- Consider implementing database migration scripts
- Set up automated backup schedules
- Create database seeding procedures for new environments

#### 2. Configuration Management
- Use infrastructure as code (Terraform, CloudFormation)
- Implement proper secrets management
- Document all manual configuration steps

#### 3. Monitoring and Alerting
- Set up health checks for all services
- Monitor database performance and disk space
- Implement alerting for service failures

### Deployment Checklist
- [ ] Verify database user credentials and permissions
- [ ] Create fresh database backup from source environment
- [ ] Test API endpoints after deployment
- [ ] Check for port conflicts and orphaned processes
- [ ] Verify frontend can load data from backend
- [ ] Test user authentication flows
- [ ] Confirm all demo accounts work correctly

## Automated Deployment Scripts

### Quick Start with Scripts
```bash
# 1. Verify local deployment
export DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"
python scripts/verify_deployment.py --local

# 2. Deploy to AWS (fully automated)
./scripts/deploy_to_aws.sh

# 3. Verify AWS deployment
python scripts/verify_deployment.py --aws

# 4. Compare environments
python scripts/verify_deployment.py --compare
```

### Available Scripts

#### 🚀 Deployment Automation
- **`scripts/deploy_to_aws.sh`**: Complete AWS deployment automation
- **`scripts/verify_deployment.py`**: Deployment verification and comparison
- **`backend/backup_database.py`**: Create timestamped database backups
- **`backend/restore_database.py`**: Restore database from backup files

#### 📋 Script Features
- **Backup/Restore**: Automated database synchronization between environments
- **Service Management**: Automated restart of backend and frontend services
- **Verification**: Health checks for database, API, and frontend
- **Comparison**: Data consistency checks between local and AWS
- **Error Handling**: Comprehensive error checking and rollback capabilities

#### 📁 Script Documentation
See [scripts/README.md](scripts/README.md) for detailed documentation and usage examples.

## Next Steps

After successful setup:
1. Explore the API documentation at http://localhost:8000/api/v1/docs (local) or http://54.217.173.125:8000/api/v1/docs (AWS)
2. Test user registration and login
3. Browse activities and destinations
4. Test booking flow
5. Access admin panel for content management
6. Use the automated deployment scripts for future updates