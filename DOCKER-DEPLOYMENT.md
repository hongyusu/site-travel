# Docker Deployment Guide

Complete guide for deploying the GetYourGuide clone using Docker.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 20GB+ disk space

## Quick Start

### 1. Initial Setup

```bash
# Clone repository
git clone <your-repo-url>
cd site-get-your-guide

# Copy environment file
cp .env.docker.example .env

# Edit environment variables (IMPORTANT!)
nano .env
```

**Important**: Change these values in `.env`:
- `POSTGRES_PASSWORD`: Strong database password
- `SECRET_KEY`: Generate with `openssl rand -hex 32`

### 2. Build and Start Services

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

### 3. Initialize Database

```bash
# Make init script executable
chmod +x docker-init-db.sh

# Run database initialization
./docker-init-db.sh

# Or manually:
docker-compose -f docker-compose.prod.yml exec backend python init_db.py
```

### 4. Create Admin User

```bash
docker-compose -f docker-compose.prod.yml exec backend python -c "
from app.database import SessionLocal
from app.models import User, UserRole
from app.core.security import get_password_hash

db = SessionLocal()
admin = User(
    email='admin@yourdomain.com',
    full_name='Admin User',
    password_hash=get_password_hash('ChangeThisPassword123!'),
    role=UserRole.ADMIN,
    is_active=True
)
db.add(admin)
db.commit()
print(f'Admin created: {admin.email}')
db.close()
"
```

### 5. Access Application

- **Frontend**: http://localhost (or http://localhost:3000 without nginx)
- **Backend API**: http://localhost/api (or http://localhost:8000)
- **API Docs**: http://localhost/docs

## Services Overview

The Docker setup includes:

1. **PostgreSQL** (port 5432) - Database
2. **Redis** (port 6379) - Caching
3. **Backend** (port 8000) - FastAPI application
4. **Frontend** (port 3000) - Next.js application
5. **Nginx** (port 80/443) - Reverse proxy

## Development vs Production

### Development (with hot reload)

```bash
# Use the dev compose file
docker-compose up -d

# Backend runs with --reload flag
# Frontend runs with npm run dev
```

### Production

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Optimized builds
# No source code mounting
# Production-ready configurations
```

## Common Operations

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f postgres
```

### Restart Services

```bash
# Restart all
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend
```

### Stop Services

```bash
# Stop all
docker-compose -f docker-compose.prod.yml stop

# Stop and remove containers
docker-compose -f docker-compose.prod.yml down

# Stop and remove everything (including volumes!)
docker-compose -f docker-compose.prod.yml down -v
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose -f docker-compose.prod.yml build

# Restart services with new images
docker-compose -f docker-compose.prod.yml up -d
```

## Database Management

### Backup Database

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres getyourguide > backup_$(date +%Y%m%d_%H%M%S).sql

# Or using docker exec
docker exec getyourguide_db pg_dump -U postgres getyourguide > backup.sql
```

### Restore Database

```bash
# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U postgres getyourguide < backup.sql

# Or using docker exec
docker exec -i getyourguide_db psql -U postgres getyourguide < backup.sql
```

### Access Database

```bash
# Connect to PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres getyourguide

# Or
docker exec -it getyourguide_db psql -U postgres getyourguide
```

### Reset Database

```bash
# Stop services
docker-compose -f docker-compose.prod.yml down

# Remove database volume
docker volume rm site-get-your-guide_postgres_data

# Start services and reinitialize
docker-compose -f docker-compose.prod.yml up -d
./docker-init-db.sh
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs [service-name]

# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check container details
docker inspect getyourguide_backend
```

### Database Connection Issues

```bash
# Verify database is ready
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U postgres

# Check database exists
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -l

# Test connection from backend
docker-compose -f docker-compose.prod.yml exec backend python -c "from app.database import engine; print(engine.url)"
```

### Frontend Not Loading

```bash
# Check if frontend is running
curl http://localhost:3000

# Check environment variables
docker-compose -f docker-compose.prod.yml exec frontend env | grep NEXT_PUBLIC

# Rebuild frontend
docker-compose -f docker-compose.prod.yml build frontend
docker-compose -f docker-compose.prod.yml up -d frontend
```

### Backend API Errors

```bash
# Check backend logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Test API directly
curl http://localhost:8000/docs

# Check environment variables
docker-compose -f docker-compose.prod.yml exec backend env | grep DATABASE_URL
```

### Nginx Issues

```bash
# Test nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# Reload nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload

# Check nginx logs
docker-compose -f docker-compose.prod.yml logs nginx
```

## Production Considerations

### 1. SSL/HTTPS Setup

Add SSL certificates to `nginx/ssl/` and update nginx configuration:

```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... rest of config
}
```

### 2. Environment Variables

Create a secure `.env` file:

```bash
# Generate strong secret key
openssl rand -hex 32

# Set strong passwords
POSTGRES_PASSWORD=$(openssl rand -base64 32)
```

### 3. Resource Limits

Add resource limits to `docker-compose.prod.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### 4. Health Checks

Already configured in docker-compose.prod.yml:
- PostgreSQL: Every 10s
- Redis: Every 10s
- Backend: Every 30s
- Frontend: Every 30s

### 5. Logging

Configure log rotation for Docker:

```bash
# /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

## Monitoring

### Container Stats

```bash
# Real-time stats
docker stats

# Specific container
docker stats getyourguide_backend
```

### Disk Usage

```bash
# Check Docker disk usage
docker system df

# Clean up unused resources
docker system prune -a
```

### Health Status

```bash
# Check health of all services
docker-compose -f docker-compose.prod.yml ps

# Inspect specific service health
docker inspect --format='{{.State.Health.Status}}' getyourguide_backend
```

## Backup Strategy

### Automated Backups

Create a backup script and cron job:

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/var/backups/getyourguide"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
docker exec getyourguide_db pg_dump -U postgres getyourguide > $BACKUP_DIR/db_$DATE.sql

# Backup volumes
docker run --rm -v site-get-your-guide_postgres_data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/postgres_volume_$DATE.tar.gz -C /data .

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Manual Backup

```bash
# Full backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres getyourguide > full_backup.sql
```

## Security Checklist

- [ ] Changed default passwords
- [ ] Generated strong SECRET_KEY
- [ ] Enabled SSL/HTTPS
- [ ] Restricted network access
- [ ] Configured firewall
- [ ] Set up regular backups
- [ ] Enabled Docker security features
- [ ] Limited container resources
- [ ] Regular security updates
- [ ] Monitoring configured

## Performance Tuning

### PostgreSQL

```yaml
postgres:
  environment:
    POSTGRES_SHARED_BUFFERS: 256MB
    POSTGRES_EFFECTIVE_CACHE_SIZE: 1GB
    POSTGRES_WORK_MEM: 16MB
```

### Backend

```yaml
backend:
  environment:
    WORKERS: 4  # Number of Uvicorn workers
```

### Nginx

Enable caching and compression in nginx.conf

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          ssh user@server 'cd /app && git pull && docker-compose -f docker-compose.prod.yml up -d --build'
```

## Scaling

### Horizontal Scaling

Add more backend instances:

```yaml
backend:
  deploy:
    replicas: 3
```

### Load Balancing

Update nginx upstream:

```nginx
upstream backend {
    server backend_1:8000;
    server backend_2:8000;
    server backend_3:8000;
}
```

## Support

For issues:
1. Check logs first
2. Verify all services are healthy
3. Review environment variables
4. Test each service independently
