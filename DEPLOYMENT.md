# Deployment Guide

This guide covers deploying the GetYourGuide clone application to a new server.

## Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Domain name (optional, but recommended)
- SSH access to the server
- sudo privileges

## Server Requirements

- 2+ CPU cores
- 4GB+ RAM
- 20GB+ disk space
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+
- Nginx

## Quick Deployment Steps

### 1. Initial Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y git curl wget build-essential nginx postgresql postgresql-contrib

# Install Python 3.12 (if not available)
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installations
python3.12 --version
node --version
npm --version
psql --version
```

### 2. Setup PostgreSQL Database

```bash
# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql <<EOF
CREATE DATABASE getyourguide;
CREATE USER getyourguide_user WITH PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE getyourguide TO getyourguide_user;
\q
EOF
```

### 3. Clone and Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/getyourguide
sudo chown $USER:$USER /var/www/getyourguide
cd /var/www/getyourguide

# Clone repository
git clone <your-repo-url> .
# Or upload files via SCP/SFTP

# Setup backend
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
cat > .env <<EOF
DATABASE_URL=postgresql://getyourguide_user:your_secure_password_here@localhost:5432/getyourguide
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:3000","http://your-domain.com","https://your-domain.com"]
EOF

# Initialize database
python init_db.py

# Setup frontend
cd ../frontend
npm install
npm run build

# Create production environment file
cat > .env.local <<EOF
NEXT_PUBLIC_API_URL=http://your-domain.com/api
EOF
```

### 4. Setup Systemd Services

#### Backend Service

```bash
sudo cat > /etc/systemd/system/getyourguide-backend.service <<EOF
[Unit]
Description=GetYourGuide Backend API
After=network.target postgresql.service

[Service]
Type=simple
User=$USER
WorkingDirectory=/var/www/getyourguide/backend
Environment="PATH=/var/www/getyourguide/backend/venv/bin"
ExecStart=/var/www/getyourguide/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start backend service
sudo systemctl daemon-reload
sudo systemctl enable getyourguide-backend
sudo systemctl start getyourguide-backend
sudo systemctl status getyourguide-backend
```

#### Frontend Service (using PM2)

```bash
# Install PM2 globally
sudo npm install -g pm2

# Start frontend
cd /var/www/getyourguide/frontend
pm2 start npm --name "getyourguide-frontend" -- start
pm2 save
pm2 startup
```

### 5. Configure Nginx

```bash
sudo cat > /etc/nginx/sites-available/getyourguide <<'EOF'
# Backend API
upstream backend {
    server 127.0.0.1:8000;
}

# Frontend
upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 10M;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend docs
    location /docs {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/getyourguide /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Setup SSL with Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal is set up automatically
sudo certbot renew --dry-run
```

### 7. Configure Firewall

```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

## Docker Deployment (Alternative)

### Prerequisites
- Docker
- Docker Compose

### Deployment Steps

```bash
# Clone repository
git clone <your-repo-url>
cd site-get-your-guide

# Update environment variables in docker-compose.yml
# Edit DATABASE_URL, SECRET_KEY, etc.

# Build and start containers
docker-compose up -d

# Initialize database
docker-compose exec backend python init_db.py

# View logs
docker-compose logs -f
```

## Post-Deployment

### 1. Verify Services

```bash
# Check backend
curl http://localhost:8000/docs

# Check frontend
curl http://localhost:3000

# Check database connection
sudo -u postgres psql getyourguide -c "SELECT COUNT(*) FROM users;"
```

### 2. Create Admin Account

```bash
cd /var/www/getyourguide/backend
source venv/bin/activate

# Run Python to create admin user
python3 <<EOF
from app.database import SessionLocal
from app.models import User, UserRole
from app.core.security import get_password_hash

db = SessionLocal()

admin = User(
    email="admin@yourdomain.com",
    full_name="Admin User",
    password_hash=get_password_hash("change_this_password"),
    role=UserRole.ADMIN,
    is_active=True
)
db.add(admin)
db.commit()
print(f"Admin user created: {admin.email}")
db.close()
EOF
```

### 3. Setup Monitoring

```bash
# Install monitoring tools
sudo apt install -y htop iotop

# Setup log rotation
sudo cat > /etc/logrotate.d/getyourguide <<EOF
/var/www/getyourguide/backend/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

### 4. Backup Strategy

```bash
# Create backup script
sudo cat > /usr/local/bin/backup-getyourguide.sh <<'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/getyourguide"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
sudo -u postgres pg_dump getyourguide > $BACKUP_DIR/db_$DATE.sql

# Backup application files
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /var/www/getyourguide

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

sudo chmod +x /usr/local/bin/backup-getyourguide.sh

# Setup daily cron job
echo "0 2 * * * /usr/local/bin/backup-getyourguide.sh" | sudo crontab -
```

## Troubleshooting

### Backend Not Starting

```bash
# Check logs
sudo journalctl -u getyourguide-backend -n 50

# Check if port 8000 is in use
sudo lsof -i :8000

# Restart service
sudo systemctl restart getyourguide-backend
```

### Frontend Not Starting

```bash
# Check PM2 logs
pm2 logs getyourguide-frontend

# Restart frontend
pm2 restart getyourguide-frontend
```

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U getyourguide_user -d getyourguide -h localhost

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Restart nginx
sudo systemctl restart nginx
```

## Performance Optimization

### 1. Enable Gzip Compression (Nginx)

Add to nginx configuration:
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

### 2. Setup Redis Caching (Optional)

```bash
# Install Redis
sudo apt install -y redis-server

# Update backend to use Redis
pip install redis
```

### 3. Database Optimization

```bash
# Connect to database
sudo -u postgres psql getyourguide

# Create indexes
CREATE INDEX idx_activities_slug ON activities(slug);
CREATE INDEX idx_activities_destination ON activities(destination_id);
CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_reviews_activity ON reviews(activity_id);
```

## Security Checklist

- [ ] Change default admin password
- [ ] Use strong SECRET_KEY
- [ ] Enable SSL/HTTPS
- [ ] Configure firewall (UFW)
- [ ] Disable root SSH login
- [ ] Setup fail2ban
- [ ] Keep system packages updated
- [ ] Regular backups enabled
- [ ] Database user has minimum required permissions
- [ ] Environment variables secured

## Updating the Application

```bash
# Pull latest changes
cd /var/www/getyourguide
git pull origin main

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart getyourguide-backend

# Update frontend
cd ../frontend
npm install
npm run build
pm2 restart getyourguide-frontend
```

## Monitoring & Logs

```bash
# Backend logs
sudo journalctl -u getyourguide-backend -f

# Frontend logs
pm2 logs getyourguide-frontend

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

## Support

For issues and questions:
- Check logs first
- Review troubleshooting section
- Ensure all services are running
- Verify database connectivity
