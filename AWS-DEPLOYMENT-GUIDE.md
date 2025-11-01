# AWS EC2 Deployment Guide

## Deployment Information

**Instance**: `ec2-54-78-136-48.eu-west-1.compute.amazonaws.com`
**Region**: eu-west-1 (Ireland)
**OS**: Ubuntu 22.04 LTS
**SSH Key**: `ocrbot.pem`

## Quick Access

```bash
# SSH Access
ssh -i "ocrbot.pem" ubuntu@ec2-54-78-136-48.eu-west-1.compute.amazonaws.com

# Application Directory
cd /home/ubuntu/getyourguide
```

## Service URLs

- **Frontend**: http://54.78.136.48:3000
- **Backend API**: http://54.78.136.48:8000
- **API Documentation**: http://54.78.136.48:8000/docs

## Demo Accounts

### Admin Account
- Email: `admin@getyourguide.com`
- Password: `admin123`
- Access: Full platform administration

### Customer Account
- Email: `customer@example.com`
- Password: `customer123`
- Access: Browse, book activities, write reviews

### Vendor Account
- Email: `vendor1@example.com`
- Password: `vendor123`
- Access: Manage activities, handle bookings

## Deployment Status

### ✅ Completed Phases

1. **Phase 1: SSH & Connection** - Verified SSH access
2. **Phase 2: Server Preparation** - Installed Docker, configured firewall
3. **Phase 3: Code Deployment** - Transferred all application files
4. **Phase 4: Environment Configuration** - Generated secrets, configured .env

### 🔄 In Progress

5. **Phase 5: Docker Build & Start** - Building images and starting containers

### ⏳ Pending

6. **Phase 6: Testing & Backups** - Health checks, backup configuration

## Server Configuration

### Docker Services

```yaml
services:
  - postgres:15-alpine (Database)
  - redis:7-alpine (Caching)
  - backend (FastAPI - Python 3.12)
  - frontend (Next.js 14 - Node 20)
  - nginx:1.25 (Reverse Proxy)
```

### Firewall Rules (UFW)

```bash
Port 22  - SSH
Port 80  - HTTP
Port 443 - HTTPS
Port 3000 - Frontend (Direct)
Port 8000 - Backend API (Direct)
```

### Environment Variables

Production secrets have been generated and configured:
- `SECRET_KEY` - 64-character random hex
- `POSTGRES_PASSWORD` - 32-character random base64
- `PYTHON_ENV=production`
- `NODE_ENV=production`

## Management Commands

### Docker Operations

```bash
# Check container status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Stop services
docker-compose -f docker-compose.prod.yml down

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

### Database Operations

```bash
# Initialize database with demo data
./docker-init-db.sh

# Create backup
./backup.sh

# Restore from backup
./backup.sh restore backups/backup-YYYYMMDD-HHMMSS.sql.gz

# List backups
./backup.sh list
```

### Application Updates

```bash
# Pull latest changes
cd /home/ubuntu/getyourguide
git pull origin main  # If using git

# Rebuild and restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Check Service Health

```bash
# Backend health
curl http://localhost:8000/docs

# Frontend health
curl http://localhost:3000

# Database connection
docker exec getyourguide_backend python -c "from app.database import SessionLocal; db = SessionLocal(); db.close(); print('OK')"
```

### View Specific Logs

```bash
# Backend logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Frontend logs
docker-compose -f docker-compose.prod.yml logs -f frontend

# Database logs
docker-compose -f docker-compose.prod.yml logs -f postgres
```

### Restart Individual Services

```bash
docker-compose -f docker-compose.prod.yml restart backend
docker-compose -f docker-compose.prod.yml restart frontend
docker-compose -f docker-compose.prod.yml restart postgres
```

## Security Considerations

### Current Setup
- ✅ SSH key-based authentication
- ✅ UFW firewall configured
- ✅ Strong random secrets generated
- ✅ Non-root users in containers
- ✅ Resource limits configured

### Recommended Improvements
- [ ] Configure domain name with DNS
- [ ] Set up SSL/TLS with Let's Encrypt
- [ ] Configure Nginx as reverse proxy (ports 80/443)
- [ ] Close direct access to ports 3000/8000
- [ ] Set up automated backups to S3
- [ ] Configure CloudWatch monitoring
- [ ] Set up log aggregation
- [ ] Enable AWS Security Groups
- [ ] Configure fail2ban for SSH protection

## Backup Strategy

### Automated Backups

Cron job configured for daily backups at 2 AM UTC:
```bash
0 2 * * * cd /home/ubuntu/getyourguide && ./backup.sh
```

### Manual Backup

```bash
cd /home/ubuntu/getyourguide
./backup.sh
```

Backups are stored in `/home/ubuntu/getyourguide/backups/`

### Backup Retention

- Local: 7 days (configurable via BACKUP_RETENTION_DAYS in .env)
- S3: Optional (configure BACKUP_S3_ENABLED and BACKUP_S3_BUCKET)

## Monitoring

### Health Check Endpoints

- Backend: `http://54.78.136.48:8000/docs`
- Frontend: `http://54.78.136.48:3000`

### Container Health

```bash
# Check all containers
docker ps

# Check specific container health
docker inspect getyourguide_backend | grep -A 10 Health
```

### Resource Usage

```bash
# Container stats
docker stats

# Disk usage
df -h

# Memory usage
free -h
```

## Scaling Considerations

### Current Configuration
- Backend: 4 Uvicorn workers
- Database: 2GB RAM limit, 2 CPU limit
- Frontend: Single instance
- Redis: 512MB memory limit

### Vertical Scaling
- Upgrade EC2 instance type
- Adjust Docker resource limits in docker-compose.prod.yml

### Horizontal Scaling
- Add load balancer (AWS ALB/NLB)
- Run multiple backend/frontend instances
- Use RDS for managed database
- Use ElastiCache for managed Redis

## Next Steps

1. **SSL/HTTPS Setup**
   ```bash
   # Install Certbot
   sudo apt-get update
   sudo apt-get install certbot python3-certbot-nginx

   # Get certificate (requires domain)
   sudo certbot --nginx -d yourdomain.com
   ```

2. **Domain Configuration**
   - Point A record to 54.78.136.48
   - Update CORS_ORIGINS in .env
   - Update NEXT_PUBLIC_API_URL in .env

3. **Monitoring Setup**
   - Configure CloudWatch agent
   - Set up application logging
   - Configure alerts for errors

4. **Performance Optimization**
   - Enable Nginx caching
   - Configure CDN for static assets
   - Optimize database queries
   - Set up Redis caching

## Support & Maintenance

### Regular Maintenance Tasks

**Daily**: Check application logs, verify backups
**Weekly**: Review security updates, check disk space
**Monthly**: Update dependencies, security audit
**Quarterly**: Rotate secrets, review access logs

### Getting Help

- Documentation: `/home/ubuntu/getyourguide/README.md`
- API Documentation: http://54.78.136.48:8000/docs
- Logs: `docker-compose -f docker-compose.prod.yml logs`

## Deployment Checklist

- [x] Server preparation (Docker, firewall)
- [x] Code deployment
- [x] Environment configuration
- [x] Secrets generation
- [ ] Docker containers built and running
- [ ] Database initialized
- [ ] Health checks passing
- [ ] Backup configured
- [ ] SSL/HTTPS (optional)
- [ ] Domain configured (optional)
- [ ] Monitoring enabled (optional)

---

**Last Updated**: 2025-11-01
**Deployment Script**: `deploy-aws.sh`
**Server Location**: `/home/ubuntu/getyourguide`
