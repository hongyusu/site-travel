# FindTravelMate - Docker Setup Guide

> **Consolidates**: DOCKER-QUICKSTART.md and Docker sections from other guides

This guide provides step-by-step instructions to run the FindTravelMate travel website using Docker containers.

## Prerequisites

- Docker Desktop (version 4.0+)
- Docker Compose (included with Docker Desktop)
- Git

## Overview

The FindTravelMate platform consists of:
- **Backend**: FastAPI application (Python) - Container
- **Frontend**: Next.js application (TypeScript/React) - Container  
- **Database**: PostgreSQL - Container
- **Redis**: Cache layer - Container
- **Admin Tools**: pgAdmin and Redis Commander - Containers

## Quick Start (Development Mode)

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd site-travel
```

### 2. Start All Services
```bash
# Start all services in development mode
docker-compose -f docker-compose.dev.yml up -d
```

This will start:
- PostgreSQL database on port 5432
- Redis cache on port 6379
- Backend API on port 8000
- Frontend app on port 3000
- pgAdmin on port 5050
- Redis Commander on port 8081

### 3. Initialize Database
```bash
# Wait for services to be healthy (about 30 seconds)
docker-compose -f docker-compose.dev.yml logs backend

# Initialize database with sample data
docker-compose -f docker-compose.dev.yml exec backend python init_db.py
```

### 4. Access the Application
- **Website**: http://localhost:3000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **Database Admin**: http://localhost:5050 (admin@findtravelmate.local / admin123)
- **Redis Admin**: http://localhost:8081

## Manual Setup (Step by Step)

### Step 1: Database Only Setup

If you want to run only the database in Docker and backend/frontend locally:

```bash
# Start only PostgreSQL and Redis
docker-compose up -d postgres redis
```

Wait for services to be healthy:
```bash
docker-compose logs postgres
# Look for: "database system is ready to accept connections"
```

### Step 2: Update Docker Compose for FindTravelMate

If using older docker compose files, they may reference old "getyourguide" names. Update the service names:

```bash
# Create updated docker-compose file
cp docker-compose.dev.yml docker-compose.findtravelmate.yml
```

Then manually update the database names in the new file to use "findtravelmate" instead of any legacy names.

### Step 3: Initialize Database with Sample Data

```bash
# Option A: If backend is running in Docker
docker-compose exec backend python init_db.py

# Option B: If backend is running locally
cd backend
python init_db.py
```

### Step 4: Verify Services

```bash
# Check all services are running
docker-compose ps

# Check service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

## Production Deployment

### 1. Build Production Images
```bash
# Build all production images
docker-compose -f docker-compose.prod.yml build
```

### 2. Start Production Services
```bash
# Start in production mode
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Initialize Production Database
```bash
# Initialize database
docker-compose -f docker-compose.prod.yml exec backend python init_db.py
```

## Environment Configuration

### Development Environment Variables

Create `.env.dev` file in project root:
```env
# Database
POSTGRES_PASSWORD=dev_password_123
POSTGRES_USER=postgres
POSTGRES_DB=findtravelmate

# Backend
SECRET_KEY=dev-secret-key-please-change-in-production
DATABASE_URL=postgresql://postgres:dev_password_123@postgres:5432/findtravelmate
APP_NAME=FindTravelMate
CORS_ORIGINS=["http://localhost:3000","http://frontend:3000"]

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Admin Tools
PGADMIN_EMAIL=admin@findtravelmate.local
PGADMIN_PASSWORD=admin123
```

### Production Environment Variables

Create `.env.prod` file in project root:
```env
# Database (Use strong passwords in production)
POSTGRES_PASSWORD=your_strong_password_here
POSTGRES_USER=postgres
POSTGRES_DB=findtravelmate

# Backend
SECRET_KEY=your-very-long-secret-key-change-this-in-production-make-it-very-secure
DATABASE_URL=postgresql://postgres:your_strong_password_here@postgres:5432/findtravelmate
APP_NAME=FindTravelMate
CORS_ORIGINS=["https://yourdomain.com"]

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api/v1
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

### Manual Database Initialization

```bash
# Method 1: Using Docker exec
docker-compose exec backend python init_db.py

# Method 2: Using Docker run (if containers aren't running)
docker-compose run --rm backend python init_db.py

# Method 3: Connect to database directly
docker-compose exec postgres psql -U postgres -d findtravelmate
```

## Service Management

### Start Services
```bash
# Development mode (with hot reload)
docker-compose -f docker-compose.dev.yml up -d

# Production mode
docker-compose -f docker-compose.prod.yml up -d

# Start specific services only
docker-compose up -d postgres redis
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This deletes data)
docker-compose down -v

# Stop specific services
docker-compose stop backend frontend
```

### View Logs
```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

### Restart Services
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend
```

## Troubleshooting

### Common Issues

#### 1. Services Not Starting
```bash
# Check service status
docker-compose ps

# View service logs for errors
docker-compose logs backend
docker-compose logs frontend

# Check Docker resources
docker system df
docker system prune  # Clean up unused resources
```

#### 2. Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Test database connection
docker-compose exec postgres pg_isready -U postgres

# Connect to database manually
docker-compose exec postgres psql -U postgres -d findtravelmate -c "\dt"
```

#### 3. Frontend Cannot Connect to Backend
**Cause**: Incorrect API URL configuration
**Solution**: Verify environment variables:
```bash
# Check frontend environment
docker-compose exec frontend env | grep NEXT_PUBLIC_API_URL

# Should show: NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

#### 4. Port Conflicts
**Cause**: Ports already in use on host machine
**Solutions**:
```bash
# Check which process is using port
lsof -i :3000
lsof -i :8000
lsof -i :5432

# Update docker-compose.yml to use different ports
# Change "3000:3000" to "3001:3000" for frontend
# Change "8000:8000" to "8001:8000" for backend
```

#### 5. Build Failures
```bash
# Clear Docker build cache
docker builder prune

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker-compose config
```

#### 6. Volume Permission Issues
```bash
# Fix volume permissions (Linux/Mac)
sudo chown -R $USER:$USER ./backend
sudo chown -R $USER:$USER ./frontend

# Reset volumes
docker-compose down -v
docker-compose up -d
```

## Data Persistence

### Database Data
- **Location**: Docker volume `postgres_data` or `postgres_dev_data`
- **Backup**: `docker-compose exec postgres pg_dump -U postgres findtravelmate > backup.sql`
- **Restore**: `docker-compose exec -T postgres psql -U postgres findtravelmate < backup.sql`

### Redis Data
- **Location**: Docker volume `redis_data` or `redis_dev_data`
- **Backup**: `docker-compose exec redis redis-cli SAVE`

### Logs
- **Container logs**: `docker-compose logs > all_logs.txt`
- **Application logs**: Stored in container `/app/logs/` directory

## Development Workflow

### 1. Start Development Environment
```bash
# Start all services
docker-compose -f docker-compose.dev.yml up -d

# Initialize database (first time only)
docker-compose -f docker-compose.dev.yml exec backend python init_db.py

# Check all services are healthy
docker-compose -f docker-compose.dev.yml ps
```

### 2. Code Changes
- **Backend**: Code changes automatically reload (volume mounted)
- **Frontend**: Code changes automatically reload (volume mounted)
- **Database**: Changes persist in Docker volume

### 3. Debugging
```bash
# View real-time logs
docker-compose -f docker-compose.dev.yml logs -f backend

# Execute commands in containers
docker-compose -f docker-compose.dev.yml exec backend python -c "print('Hello')"
docker-compose -f docker-compose.dev.yml exec frontend npm run lint

# Access container shell
docker-compose -f docker-compose.dev.yml exec backend bash
docker-compose -f docker-compose.dev.yml exec frontend sh
```

### 4. Database Management
```bash
# Access pgAdmin at http://localhost:5050
# Username: admin@findtravelmate.local
# Password: admin123

# Direct database access
docker-compose -f docker-compose.dev.yml exec postgres psql -U postgres -d findtravelmate
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

## Performance Optimization

### Resource Limits
Add to docker-compose.yml:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### Health Checks
All services include health checks:
```bash
# Check service health
docker-compose ps
# Look for "healthy" status
```

## Security Considerations

### Development
- Default passwords are used (change for production)
- Services expose ports on localhost only
- Debug mode enabled

### Production
- Use strong, unique passwords
- Configure proper CORS origins
- Use HTTPS/TLS certificates
- Limit exposed ports
- Enable Docker security scanning
- Regular security updates

## Next Steps

After successful Docker setup:
1. Access the application at http://localhost:3000
2. Explore the API documentation at http://localhost:8000/api/v1/docs
3. Manage database via pgAdmin at http://localhost:5050
4. Monitor Redis via Redis Commander at http://localhost:8081
5. Test user registration and login flows
6. Customize configuration for your deployment needs