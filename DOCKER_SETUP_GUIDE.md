# FindTravelMate - Docker Setup Guide

This guide provides streamlined, tested instructions for running FindTravelMate using Docker in both development and production environments.

## Prerequisites

- Docker Desktop (version 4.0+)
- Docker Compose (included with Docker Desktop)
- Git

## Architecture Overview

The FindTravelMate platform uses different Docker configurations for different environments:

### Development Environment (2-file approach)

- **`docker-compose.services.yml`**: Database (PostgreSQL) + Redis only
- **`docker-compose.dev.yml`**: Backend + Frontend containers (connects to services)

### Production Environment (1-file approach)  

- **`docker-compose.yml`**: Complete stack with Nginx reverse proxy

**Services:**

- **Backend**: FastAPI application (Python)
- **Frontend**: Next.js application (TypeScript/React)  
- **Database**: PostgreSQL 15
- **Redis**: Cache layer
- **Nginx**: Reverse proxy (production only)

## Development Setup

### Quick Start (Proven Workflow)

```bash
# 1. Clone and navigate to project
git clone <repository-url>
cd site-travel

# 2. Start database services first
docker-compose -f docker-compose.services.yml up -d

# 3. Start development containers
docker-compose -f docker-compose.dev.yml up -d

# 4. Wait for services to be healthy (about 30 seconds)
docker-compose -f docker-compose.dev.yml logs -f
```

### Access Points

- **Frontend**: <http://localhost:3000>
- **Backend API**: <http://localhost:8000>
- **API Documentation**: <http://localhost:8000/docs>
- **Database**: localhost:5432 (postgres/password)
- **Redis**: localhost:6379

### Database Initialization

The backend automatically initializes the database with sample data on first connection.

- **Activities**: ~21 sample activities
- **Users**: Admin, customer, and vendor accounts
- **Categories**: 10 activity categories

### Development Features

- **Hot Reload**: Code changes automatically reload
- **Debug Mode**: Detailed logging enabled
- **Direct Access**: All services accessible on host ports

## Production Setup

### Quick Start (Single Command)

```bash
# 1. Clone and navigate to project
git clone <repository-url>
cd site-travel

# 2. Configure environment variables
cp .env.production .env
# Edit .env with your production values

# 3. Deploy complete stack
docker-compose up -d --build

# 4. Check deployment status
docker-compose ps
```

### Production Features

- **Nginx Reverse Proxy**: All traffic routed through nginx (ports 80/443)
- **Security**: No direct database/redis/backend port exposure
- **Resource Limits**: CPU and memory limits configured
- **Health Checks**: Automatic service health monitoring
- **Logging**: Structured logging with rotation
- **SSL Ready**: SSL certificate mounting supported

### Access Points (Production)

- **Application**: <http://your-domain> (via nginx only)
- **No Direct Access**: Database, Redis, Backend only accessible internally

### Database Restoration (Production)

```bash
# 1. Place backup file in ./backups/ directory
cp your_backup.sql ./backups/

# 2. Restore database
docker-compose exec postgres psql -U postgres -d findtravelmate -f /backups/your_backup.sql

# 3. Verify restoration
docker-compose exec postgres psql -U postgres -d findtravelmate -c "SELECT count(*) FROM activities;"
```

## Service Management

### Development Commands

```bash
# Start services only (database + redis)
docker-compose -f docker-compose.services.yml up -d

# Start development containers
docker-compose -f docker-compose.dev.yml up -d

# Stop development containers (keeps services running)
docker-compose -f docker-compose.dev.yml down

# Stop all development services
docker-compose -f docker-compose.services.yml down
docker-compose -f docker-compose.dev.yml down

# View logs
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.services.yml logs -f postgres

# Check service status
docker-compose -f docker-compose.services.yml ps
docker-compose -f docker-compose.dev.yml ps
```

### Production Commands

```bash
# Deploy production stack
docker-compose up -d --build

# Stop production stack
docker-compose down

# View production logs
docker-compose logs -f nginx
docker-compose logs -f backend

# Check production status
docker-compose ps

# Scale services (if needed)
docker-compose up -d --scale backend=2
```

### Database Management

```bash
# Development - Direct database access
docker-compose -f docker-compose.services.yml exec postgres psql -U postgres -d findtravelmate

# Production - Database access
docker-compose exec postgres psql -U postgres -d findtravelmate

# Backup database
docker-compose exec postgres pg_dump -U postgres findtravelmate > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
docker-compose exec -T postgres psql -U postgres -d findtravelmate < your_backup.sql
```

## Environment Configuration

### Development Environment Variables

Development uses default values from docker-compose files:

- **Database**: postgres/password@localhost:5432
- **Redis**: localhost:6379
- **Backend**: Debug logging, auto-reload enabled
- **Frontend**: Development mode with hot reload

**Optional `.env.dev` file for customization:**

```env
# Only needed if you want to override defaults
POSTGRES_PASSWORD=custom_dev_password
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
LOG_LEVEL=DEBUG
```

### Production Environment Variables

**Required `.env` file for production:**

```env
# Database (Use strong passwords)
POSTGRES_PASSWORD=your_secure_production_password_here

# Backend Security
SECRET_KEY=your-very-long-secret-key-minimum-32-characters-change-this
CORS_ORIGINS=["https://yourdomain.com"]

# Frontend
NEXT_PUBLIC_API_URL=https://yourdomain.com/api/v1

# Optional Performance Tuning
DB_POOL_SIZE=20
LOG_LEVEL=INFO
```

## Database Initialization

**Automatic Initialization:**
The backend automatically initializes the database on first connection with:

- All required database tables
- Admin user: `admin@findtravelmate.com` / `admin123`
- Customer user: `customer@example.com` / `customer123`  
- 5 Vendor accounts: `vendor1-5@example.com` / `vendor123`
- 21 sample activities across 10 destinations
- 8 activity categories
- Sample reviews and bookings

**Manual Initialization (if needed):**

```bash
# Development environment
docker-compose -f docker-compose.dev.yml exec backend python init_db.py

# Production environment
docker-compose exec backend python init_db.py

# Direct database access
docker-compose exec postgres psql -U postgres -d findtravelmate
```

## Common Operations

### Viewing Logs

```bash
# Development - View all logs
docker-compose -f docker-compose.dev.yml logs -f

# Development - Specific service logs
docker-compose -f docker-compose.services.yml logs postgres
docker-compose -f docker-compose.dev.yml logs backend

# Production - View all logs
docker-compose logs -f

# Production - Specific service logs
docker-compose logs nginx
docker-compose logs backend
```

### Service Health Checks

```bash
# Check service status
docker-compose ps

# Health check details
docker inspect <container_name> | grep -A 10 Health
```

### Restarting Services

```bash
# Development - Restart specific services
docker-compose -f docker-compose.dev.yml restart backend
docker-compose -f docker-compose.services.yml restart postgres

# Production - Restart services
docker-compose restart backend
docker-compose restart nginx
```

## Troubleshooting

### Common Issues

#### 1. Services Not Starting

```bash
# Check all service status
docker-compose ps

# View logs for startup errors
docker-compose logs <service_name>

# Clean up Docker resources
docker system prune -f
```

#### 2. Database Connection Issues (Development)

```bash
# Ensure services are running first
docker-compose -f docker-compose.services.yml ps

# Test database connectivity
docker-compose -f docker-compose.services.yml exec postgres pg_isready -U postgres

# Check database tables
docker-compose -f docker-compose.services.yml exec postgres psql -U postgres -d findtravelmate -c "\dt"
```

#### 3. Backend Cannot Connect to Database

**Development**: Ensure `docker-compose.services.yml` is running first

```bash
# Start services first
docker-compose -f docker-compose.services.yml up -d
# Then start development containers
docker-compose -f docker-compose.dev.yml up -d
```

#### 4. Frontend Cannot Load

**Check API connectivity:**

```bash
# Test backend health from host
curl http://localhost:8000/api/v1/activities/categories

# Check frontend environment
docker-compose exec frontend env | grep NEXT_PUBLIC_API_URL
```

#### 5. Port Conflicts

```bash
# Check what's using common ports
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# Kill conflicting processes or change ports in docker-compose files
```

#### 6. Production Nginx Issues

```bash
# Check nginx configuration
docker-compose exec nginx nginx -t

# View nginx logs
docker-compose logs nginx

# Restart nginx
docker-compose restart nginx
```

## Data Persistence

### Development Data

- **Database**: Volume `postgres_data` (shared between service and dev containers)
- **Redis**: Volume `redis_data`
- **Frontend**: Volume `frontend_next_cache` (build cache)
- **Backend**: Volume `backend_logs`

### Production Data

- **Database**: Volume `postgres_data` with backup directory mounted
- **Redis**: Volume `redis_data`
- **Nginx**: Volumes `nginx_logs` and `nginx_cache`
- **Backend**: Volume `backend_logs`

### Backup & Restore

```bash
# Create database backup
docker-compose exec postgres pg_dump -U postgres findtravelmate > backup_$(date +%Y%m%d).sql

# Restore from backup (production)
cp backup.sql ./backups/
docker-compose exec postgres psql -U postgres -d findtravelmate < /backups/backup.sql

# Development restore
docker-compose -f docker-compose.services.yml exec postgres psql -U postgres -d findtravelmate < /backups/backup.sql
```

## Development Workflow

### 1. Start Development Environment

```bash
# Step 1: Start database services
docker-compose -f docker-compose.services.yml up -d

# Step 2: Wait for services to be healthy (30 seconds)
docker-compose -f docker-compose.services.yml logs -f

# Step 3: Start development containers
docker-compose -f docker-compose.dev.yml up -d

# Step 4: Check all services
docker-compose -f docker-compose.dev.yml ps
```

### 2. Code Development

- **Backend**: Hot reload enabled, logs via `docker-compose -f docker-compose.dev.yml logs -f backend`
- **Frontend**: Hot reload enabled, accessible at <http://localhost:3000>
- **Database**: Persistent data, accessible at localhost:5432

### 3. Development Commands

```bash
# Backend debugging
docker-compose -f docker-compose.dev.yml exec backend python -c "import app; print('Backend OK')"

# Frontend debugging  
docker-compose -f docker-compose.dev.yml exec frontend npm run lint

# Database queries
docker-compose -f docker-compose.services.yml exec postgres psql -U postgres -d findtravelmate -c "SELECT count(*) FROM activities;"

# Container shell access
docker-compose -f docker-compose.dev.yml exec backend bash
```

### 4. Stopping Development Environment

```bash
# Stop development containers (keeps database running)
docker-compose -f docker-compose.dev.yml down

# Stop database services (when done for the day)
docker-compose -f docker-compose.services.yml down
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

## Resource Management

### Development Resources

- **Database**: 256M limit, 128M reserved
- **Redis**: 64M limit, 32M reserved  
- **Backend**: 512M limit, 256M reserved
- **Frontend**: 1G limit, 512M reserved

### Production Resources

- **Database**: 2G limit, 512M reserved
- **Redis**: 768M limit, 256M reserved
- **Backend**: 2G limit, 512M reserved
- **Frontend**: 1G limit, 256M reserved
- **Nginx**: 512M limit, 128M reserved

### Health Monitoring

```bash
# Check service health status
docker-compose ps

# View resource usage
docker stats

# Service-specific health checks
curl -f http://localhost:8000/api/v1/activities/categories  # Backend
curl -f http://localhost:3000  # Frontend (dev)
curl -f http://localhost     # Nginx (prod)
```

## Security Features

### Development Security

- **Database**: Default password (postgres/password)
- **Exposed Ports**: All services accessible on localhost
- **Debug Mode**: Enabled for development
- **CORS**: Permissive for development

### Production Security

- **Port Isolation**: Only nginx (80/443) exposed externally
- **Database**: No direct external access
- **Backend**: No direct external access
- **Redis**: No direct external access
- **Resource Limits**: Enforced on all services
- **Security Options**: `no-new-privileges` enabled
- **Read-only**: Containers use read-only where possible

### Production Security Checklist

- [ ] Set strong `POSTGRES_PASSWORD` in `.env`
- [ ] Set secure `SECRET_KEY` (minimum 32 characters)
- [ ] Configure `CORS_ORIGINS` for your domain
- [ ] Use HTTPS with SSL certificates
- [ ] Regular security updates for base images
- [ ] Monitor logs for suspicious activity

## Quick Reference

### Development Commands

```bash
# Start everything
docker-compose -f docker-compose.services.yml up -d
docker-compose -f docker-compose.dev.yml up -d

# Stop everything
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.services.yml down

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Production Commands

```bash
# Deploy
docker-compose up -d --build

# Stop
docker-compose down

# View logs
docker-compose logs -f nginx
```

### Access Points

**Development:**

- Frontend: <http://localhost:3000>
- Backend API: <http://localhost:8000>
- API Docs: <http://localhost:8000/docs>
- Database: localhost:5432 (postgres/password)

**Production:**

- Application: <http://your-domain> (via nginx)
- Internal services: Not directly accessible

### Test Accounts

- **Admin**: <admin@findtravelmate.com> / admin123
- **Customer**: <customer@example.com> / customer123
- **Vendor**: <vendor1@example.com> / vendor123

---

*This guide reflects the tested, working configuration used in production deployments.*
