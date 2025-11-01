# Docker Quickstart Guide - GetYourGuide Clone

**⏱️ Deployment Time:** 5 minutes from clone to running application

---

## Prerequisites

- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose V2 ([Included with Docker Desktop](https://docs.docker.com/compose/install/))
- 4GB RAM minimum, 8GB recommended
- 10GB free disk space

### Verify Prerequisites

```bash
docker --version  # Should be 20.10+
docker compose version  # Should be v2.0+
```

---

## Quick Start (5 Minutes)

### 1. Clone and Navigate

```bash
git clone https://github.com/hongyusu/site-travel.git
cd site-travel
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.docker.example .env

# Generate secure secret key
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

# (Optional) Customize database password
echo "POSTGRES_PASSWORD=$(openssl rand -base64 24)" >> .env
```

### 3. Start All Services

```bash
# Build and start all containers
docker compose -f docker-compose.prod.yml up -d --build

# This will start:
# - PostgreSQL database
# - Redis cache
# - FastAPI backend
# - Next.js frontend
# - Nginx reverse proxy
```

### 4. Initialize Database

```bash
# Run database initialization script
chmod +x docker-init-db.sh
./docker-init-db.sh

# This creates:
# - Database tables
# - Demo accounts (admin, customer, vendors)
# - Sample activities, bookings, reviews
```

### 5. Access Application

Open your browser to:

**Frontend:** http://localhost
**API Docs:** http://localhost/api/docs
**Admin Panel:** http://localhost/admin/dashboard

---

## Demo Accounts

### Admin Account
- **Email:** admin@getyourguide.com
- **Password:** admin123
- **Access:** Full platform administration

### Customer Account
- **Email:** customer@example.com
- **Password:** customer123
- **Access:** Browse, book, review activities

### Vendor Accounts
- **Email:** vendor1@example.com - vendor5@example.com
- **Password:** vendor123
- **Access:** Manage activities and bookings

---

## Common Commands

### View Logs

```bash
# All services
docker compose -f docker-compose.prod.yml logs -f

# Specific service
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f frontend
docker compose -f docker-compose.prod.yml logs -f postgres
```

### Stop Services

```bash
# Stop all services
docker compose -f docker-compose.prod.yml stop

# Stop specific service
docker compose -f docker-compose.prod.yml stop backend
```

### Restart Services

```bash
# Restart all services
docker compose -f docker-compose.prod.yml restart

# Restart specific service
docker compose -f docker-compose.prod.yml restart backend
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker compose -f docker-compose.prod.yml up -d --build

# Rebuild specific service
docker compose -f docker-compose.prod.yml up -d --build backend
```

### Clean Up Everything

```bash
# Stop and remove containers, networks
docker compose -f docker-compose.prod.yml down

# Also remove volumes (DATABASE WILL BE DELETED!)
docker compose -f docker-compose.prod.yml down -v
```

### Access Container Shell

```bash
# Backend container
docker compose -f docker-compose.prod.yml exec backend bash

# Frontend container
docker compose -f docker-compose.prod.yml exec frontend sh

# Database container
docker compose -f docker-compose.prod.yml exec postgres psql -U postgres -d getyourguide
```

---

## Service URLs

| Service | Internal | External | Description |
|---------|----------|----------|-------------|
| **Frontend** | frontend:3000 | http://localhost | Next.js application |
| **Backend** | backend:8000 | http://localhost/api | FastAPI REST API |
| **Postgres** | postgres:5432 | localhost:5432 | PostgreSQL database |
| **Redis** | redis:6379 | localhost:6379 | Redis cache |
| **Nginx** | - | http://localhost | Reverse proxy |
| **API Docs** | - | http://localhost/api/docs | Swagger UI |

---

## Troubleshooting

### Port Already in Use

**Problem:** `Error: port is already allocated`

**Solution:**
```bash
# Check what's using the port
lsof -ti:80  # or :5432, :6379, etc.

# Kill the process
kill -9 $(lsof -ti:80)

# Or change ports in docker-compose.prod.yml
```

### Container Fails to Start

**Problem:** Service keeps restarting or exits immediately

**Solution:**
```bash
# Check logs for errors
docker compose -f docker-compose.prod.yml logs backend

# Common fixes:
# 1. Check environment variables in .env
# 2. Ensure database is healthy
docker compose -f docker-compose.prod.yml ps
# 3. Rebuild containers
docker compose -f docker-compose.prod.yml up -d --build --force-recreate
```

### Database Connection Failed

**Problem:** Backend can't connect to database

**Solution:**
```bash
# Check if postgres is healthy
docker compose -f docker-compose.prod.yml ps postgres

# Wait for database to be ready (takes ~10 seconds on first start)
docker compose -f docker-compose.prod.yml logs postgres | grep "ready"

# Restart backend after postgres is ready
docker compose -f docker-compose.prod.yml restart backend
```

### Frontend Shows API Errors

**Problem:** "Failed to fetch" or API connection errors

**Solution:**
```bash
# Check backend is running
docker compose -f docker-compose.prod.yml ps backend

# Check backend logs for errors
docker compose -f docker-compose.prod.yml logs backend

# Verify backend health
curl http://localhost/api/docs

# Common fix: Rebuild with proper environment variables
docker compose -f docker-compose.prod.yml up -d --build frontend backend
```

### Out of Disk Space

**Problem:** "No space left on device"

**Solution:**
```bash
# Remove unused Docker resources
docker system prune -a --volumes

# Check Docker disk usage
docker system df

# Remove old images
docker image prune -a
```

### Permission Denied Errors

**Problem:** Permission errors when running scripts

**Solution:**
```bash
# Make scripts executable
chmod +x docker-init-db.sh
chmod +x deploy.sh
chmod +x backup.sh

# If on Linux, you may need to adjust file ownership
sudo chown -R $USER:$USER .
```

---

## Health Checks

### Verify All Services are Running

```bash
docker compose -f docker-compose.prod.yml ps
```

Expected output (all services "healthy" or "running"):
```
NAME                    STATUS          PORTS
getyourguide_backend    healthy         0.0.0.0:8000->8000/tcp
getyourguide_db         healthy         0.0.0.0:5432->5432/tcp
getyourguide_frontend   healthy         0.0.0.0:3000->3000/tcp
getyourguide_nginx      running         0.0.0.0:80->80/tcp
getyourguide_redis      healthy         0.0.0.0:6379->6379/tcp
```

### Test API Connectivity

```bash
# Health check
curl http://localhost/api/docs

# List activities
curl http://localhost/api/v1/activities/search

# Login test
curl -X POST http://localhost/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"customer@example.com","password":"customer123"}'
```

### Test Frontend

```bash
# Homepage
curl -s http://localhost | grep "MeetYourTravelPartner"

# Should return HTML with site title
```

---

##Performance Tips

### Development vs Production

**For Development:**
- Use `docker-compose.dev.yml` (with hot reload)
- Volumes mounted for live code changes
- Debug logging enabled

**For Production:**
- Use `docker-compose.prod.yml` (optimized builds)
- Standalone builds (no volumes)
- Production logging level

### Resource Allocation

Edit `docker-compose.prod.yml` to limit resources:

```yaml
backend:
  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 2G
      reservations:
        cpus: '0.5'
        memory: 512M
```

### Image Size Optimization

Current image sizes (after optimization):
- Backend: ~250MB
- Frontend: ~200MB
- Total: ~450MB

To reduce further:
```bash
# Use multi-stage builds (already implemented)
# Remove unnecessary dependencies
# Use alpine base images (already implemented)
```

---

## Next Steps

### For Development
1. Switch to development compose file: `docker-compose.dev.yml`
2. Enable hot reload for code changes
3. Install development tools in containers

### For Production Deployment
1. Configure SSL certificates in `nginx/ssl/`
2. Update CORS origins in `.env`
3. Set secure passwords and secret keys
4. Configure backup automation
5. Set up monitoring and logging

### Customization
1. Modify `nginx/nginx.conf` for custom routing
2. Add custom environment variables in `.env`
3. Configure Redis caching strategies
4. Adjust database connection pooling

---

## Getting Help

- **Documentation:** See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide
- **Architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- **API Reference:** See [API-REFERENCE.md](API-REFERENCE.md) for endpoints
- **Issues:** Report at https://github.com/hongyusu/site-travel/issues

---

## Quick Reference

### One-Line Commands

```bash
# Fresh start (delete everything and restart)
docker compose -f docker-compose.prod.yml down -v && docker compose -f docker-compose.prod.yml up -d --build && ./docker-init-db.sh

# Update code and rebuild
git pull && docker compose -f docker-compose.prod.yml up -d --build

# Backup database
docker compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres getyourguide > backup.sql

# Restore database
docker compose -f docker-compose.prod.yml exec -T postgres psql -U postgres getyourguide < backup.sql

# View real-time logs (all services)
docker compose -f docker-compose.prod.yml logs -f --tail=100
```

---

**🚀 You're all set! The application should be running at http://localhost**

**Questions?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment guide or [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.
