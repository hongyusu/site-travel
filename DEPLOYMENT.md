# Deployment Guide

Complete guide for deploying the GetYourGuide clone application locally, with Docker, or on cloud infrastructure.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Traditional Server Deployment](#traditional-server-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Post-Deployment](#post-deployment)
6. [Maintenance & Operations](#maintenance--operations)

---

## Local Development

### Prerequisites

- Python 3.12+ with pyenv
- Node.js 18+
- PostgreSQL 14+
- Git

### macOS Setup

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install postgresql@14 pyenv node

# Start PostgreSQL
brew services start postgresql@14

# Install Python 3.12
pyenv install 3.12.8
```

### Linux (Ubuntu) Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Python 3.12
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Database Setup

```bash
# macOS
createdb getyourguide

# Ubuntu
sudo -u postgres createdb getyourguide
sudo -u postgres psql -c "CREATE USER getyourguide_user WITH PASSWORD 'dev_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE getyourguide TO getyourguide_user;"
```

### Clone Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd site-travel

# Or if you already have it
cd /path/to/site-travel
```

### Backend Setup

```bash
cd backend

# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
cat > .env <<EOF
DATABASE_URL=postgresql://postgres:@localhost:5432/getyourguide
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:3000"]
EOF

# Initialize database
python init_db.py

# Start backend server
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Create .env.local
cat > .env.local <<EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api
EOF

# Start frontend
npm run dev
```

### Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Demo Accounts

After running `init_db.py`, the following accounts are available:

- **Admin**: admin@getyourguide.com / admin123
- **Customer**: customer@example.com / customer123
- **Vendor**: vendor1@example.com / vendor123

---

## Docker Deployment

Complete guide for deploying with Docker - fastest way to get started!

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 20GB+ disk space

Install Docker:
- **macOS**: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Ubuntu**:
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker $USER
  # Log out and back in
  ```

### Quick Start (5 Minutes)

```bash
# 1. Copy environment template
cp .env.docker.example .env

# 2. Generate secure keys
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
echo "POSTGRES_PASSWORD=$(openssl rand -base64 16)" >> .env

# 3. Start all services
docker-compose -f docker-compose.prod.yml up -d

# 4. Wait for services to be healthy (30-60 seconds)
docker-compose -f docker-compose.prod.yml ps

# 5. Initialize database
chmod +x docker-init-db.sh
./docker-init-db.sh

# 6. Create admin user
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
print(f'✅ Admin created: {admin.email}')
db.close()
"

# 7. Access application
open http://localhost
```

### Docker Services

The setup includes 5 containerized services:

1. **PostgreSQL** (port 5432) - Database with automatic backups
2. **Redis** (port 6379) - Caching and session storage
3. **Backend** (port 8000) - FastAPI application
4. **Frontend** (port 3000) - Next.js application
5. **Nginx** (port 80/443) - Reverse proxy and load balancer

### Development vs Production

**Development Mode** (with hot reload):
```bash
# Start dev environment
docker-compose up -d

# Backend runs with --reload flag
# Frontend runs with npm run dev
# Source code is mounted as volumes for live updates
```

**Production Mode**:
```bash
# Start production environment
docker-compose -f docker-compose.prod.yml up -d

# Optimized production builds
# No source code mounting
# Production-ready configurations
# Health checks enabled
```

### Common Docker Operations

#### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f postgres
docker-compose -f docker-compose.prod.yml logs -f nginx
```

#### Restart Services
```bash
# Restart all
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend
docker-compose -f docker-compose.prod.yml restart frontend
```

#### Stop Services
```bash
# Stop all (data preserved)
docker-compose -f docker-compose.prod.yml stop

# Stop and remove containers (data preserved)
docker-compose -f docker-compose.prod.yml down

# Stop and remove everything including data (DESTRUCTIVE!)
docker-compose -f docker-compose.prod.yml down -v
```

#### Update Application
```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose -f docker-compose.prod.yml build

# Restart with new images (zero-downtime)
docker-compose -f docker-compose.prod.yml up -d
```

### Database Management

#### Backup Database
```bash
# Create timestamped backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres getyourguide > backup_$(date +%Y%m%d_%H%M%S).sql

# Or using docker exec directly
docker exec getyourguide_db pg_dump -U postgres getyourguide > backup.sql
```

#### Restore Database
```bash
# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U postgres getyourguide < backup.sql

# Or using docker exec
docker exec -i getyourguide_db psql -U postgres getyourguide < backup.sql
```

#### Access Database Console
```bash
# Connect to PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres getyourguide

# Or
docker exec -it getyourguide_db psql -U postgres getyourguide
```

#### Reset Database
```bash
# Stop services
docker-compose -f docker-compose.prod.yml down

# Remove database volume
docker volume rm site-travel_postgres_data

# Start services and reinitialize
docker-compose -f docker-compose.prod.yml up -d
./docker-init-db.sh
```

### Docker Troubleshooting

#### Service Won't Start
```bash
# Check logs for errors
docker-compose -f docker-compose.prod.yml logs [service-name]

# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check container details
docker inspect getyourguide_backend

# Check resource usage
docker stats
```

#### Database Connection Issues
```bash
# Verify database is ready
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U postgres

# Check database exists
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -l

# Test connection from backend
docker-compose -f docker-compose.prod.yml exec backend python -c "from app.database import engine; print(engine.url)"
```

#### Frontend Not Loading
```bash
# Check if frontend is running
curl http://localhost:3000

# Check environment variables
docker-compose -f docker-compose.prod.yml exec frontend env | grep NEXT_PUBLIC

# Rebuild frontend
docker-compose -f docker-compose.prod.yml build frontend
docker-compose -f docker-compose.prod.yml up -d frontend
```

#### Backend API Errors
```bash
# Check backend logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Test API directly
curl http://localhost:8000/docs

# Check environment variables
docker-compose -f docker-compose.prod.yml exec backend env | grep DATABASE_URL

# Restart backend
docker-compose -f docker-compose.prod.yml restart backend
```

#### Nginx Issues
```bash
# Test nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# Reload nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload

# Check nginx logs
docker-compose -f docker-compose.prod.yml logs nginx
```

#### Port Conflicts
```bash
# Check what's using port 80
sudo lsof -i :80

# Check what's using port 8000
lsof -i :8000

# Kill process on port
kill -9 <PID>
```

### SSL/HTTPS Setup (Docker)

Add SSL certificates and update nginx configuration:

```bash
# Create SSL directory
mkdir -p nginx/ssl

# Option 1: Use Let's Encrypt
certbot certonly --standalone -d yourdomain.com

# Copy certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem

# Option 2: Self-signed (development only)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem
```

Update `nginx/nginx.conf`:
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Strong SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers off;

    # ... rest of nginx config
}
```

### Production Considerations (Docker)

#### Environment Variables
Create secure `.env` file:
```bash
# Generate strong passwords
SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET=$(openssl rand -hex 32)

# Update .env file
cat > .env <<EOF
POSTGRES_DB=getyourguide
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/getyourguide
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["https://yourdomain.com"]
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
EOF
```

#### Resource Limits
Add to `docker-compose.prod.yml`:
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

  frontend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

#### Logging Configuration
Configure Docker log rotation in `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Restart Docker:
```bash
sudo systemctl restart docker
```

#### Automated Backups (Docker)
Create backup script `/usr/local/bin/backup-docker-getyourguide.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/getyourguide"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
docker exec getyourguide_db pg_dump -U postgres getyourguide > $BACKUP_DIR/db_$DATE.sql

# Backup volumes
docker run --rm \
  -v site-travel_postgres_data:/data \
  -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/postgres_volume_$DATE.tar.gz -C /data .

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "✅ Backup completed: $DATE"
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/backup-docker-getyourguide.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-docker-getyourguide.sh") | crontab -
```

---

## Traditional Server Deployment

Deploy to Ubuntu server with systemd services (no Docker required).

### Server Requirements

- Ubuntu 20.04+ or similar Linux distribution
- 2+ CPU cores
- 4GB+ RAM
- 20GB+ disk space
- Domain name (recommended)
- SSH access with sudo privileges

### 1. Initial Server Setup

```bash
# Connect to server
ssh user@your-server-ip

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y git curl wget build-essential nginx postgresql postgresql-contrib

# Install Python 3.12
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

### 2. Setup PostgreSQL

```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql <<EOF
CREATE DATABASE getyourguide;
CREATE USER getyourguide_user WITH PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE getyourguide TO getyourguide_user;
ALTER USER getyourguide_user CREATEDB;
\q
EOF

# Test connection
psql -U getyourguide_user -d getyourguide -h localhost -W
```

### 3. Deploy Application

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
CORS_ORIGINS=["https://yourdomain.com"]
EOF

# Initialize database with demo data
python init_db.py

# Test backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Press Ctrl+C after verifying it works

# Setup frontend
cd /var/www/getyourguide/frontend
npm install

# Create production environment file
cat > .env.local <<EOF
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
EOF

# Build frontend
npm run build

# Test frontend
npm start
# Press Ctrl+C after verifying it works
```

### 4. Setup Systemd Services

#### Backend Service

```bash
sudo tee /etc/systemd/system/getyourguide-backend.service > /dev/null <<EOF
[Unit]
Description=GetYourGuide Backend API
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=$USER
WorkingDirectory=/var/www/getyourguide/backend
Environment="PATH=/var/www/getyourguide/backend/venv/bin"
ExecStart=/var/www/getyourguide/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start backend service
sudo systemctl daemon-reload
sudo systemctl enable getyourguide-backend
sudo systemctl start getyourguide-backend

# Check status
sudo systemctl status getyourguide-backend
```

#### Frontend Service (using PM2)

```bash
# Install PM2 globally
sudo npm install -g pm2

# Start frontend with PM2
cd /var/www/getyourguide/frontend
pm2 start npm --name "getyourguide-frontend" -- start

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
# Follow the command it outputs (copy and run it)

# Check PM2 status
pm2 status
pm2 logs getyourguide-frontend
```

### 5. Configure Nginx

```bash
sudo tee /etc/nginx/sites-available/getyourguide > /dev/null <<'EOF'
# Backend API upstream
upstream backend {
    server 127.0.0.1:8000;
}

# Frontend upstream
upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    # Frontend (React/Next.js)
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

        # CORS headers (if needed)
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
    }

    # Backend OpenAPI docs
    location /docs {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /openapi.json {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_min_length 256;
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/getyourguide /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### 6. Setup SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate (interactive)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Or non-interactive
sudo certbot --nginx --non-interactive --agree-tos \
  -m your-email@example.com \
  -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run

# Auto-renewal is set up automatically via systemd timer
sudo systemctl status certbot.timer
```

### 7. Configure Firewall

```bash
# Enable UFW firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Check status
sudo ufw status

# Alternative: Allow specific ports
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## Cloud Deployment

### AWS Deployment

#### EC2 Setup

```bash
# 1. Launch EC2 instance
# - Ubuntu 20.04 LTS
# - t3.medium or larger (2 vCPU, 4GB RAM)
# - 20GB+ EBS storage
# - Security group: Allow 22, 80, 443

# 2. Connect to instance
ssh -i your-key.pem ubuntu@ec2-xxx.compute.amazonaws.com

# 3. Follow Traditional Server Deployment steps above
```

#### RDS Database (Recommended)

```bash
# 1. Create RDS PostgreSQL instance
# - Engine: PostgreSQL 14+
# - Instance class: db.t3.small or larger
# - Storage: 20GB+
# - Enable automated backups

# 2. Update backend .env
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/getyourguide

# 3. Run init_db.py from EC2
```

#### S3 for Static Assets (Optional)

```bash
# Store activity images, user uploads in S3
pip install boto3

# Update backend to use S3 for file uploads
```

### DigitalOcean Deployment

#### Droplet Setup

```bash
# 1. Create Droplet
# - Ubuntu 20.04 LTS
# - Basic ($24/month - 2 vCPU, 4GB RAM)
# - 80GB SSD

# 2. Enable firewall
# Allow: SSH (22), HTTP (80), HTTPS (443)

# 3. Follow Traditional Server Deployment steps
```

#### Managed Database

```bash
# 1. Create managed PostgreSQL database
# - Version: 14
# - Plan: Basic ($15/month)

# 2. Update DATABASE_URL to managed database connection string
```

### Google Cloud Platform

#### Compute Engine Setup

```bash
# 1. Create VM instance
# - Ubuntu 20.04 LTS
# - e2-standard-2 (2 vCPU, 8GB RAM)
# - 20GB+ persistent disk

# 2. Configure firewall rules
# Allow: HTTP, HTTPS, SSH

# 3. Follow Traditional Server Deployment steps
```

#### Cloud SQL

```bash
# 1. Create Cloud SQL PostgreSQL instance
# - Version: 14
# - Machine type: db-f1-micro or larger

# 2. Create database user and set password
# 3. Update DATABASE_URL with Cloud SQL connection string
```

---

## Post-Deployment

### 1. Verify Services

```bash
# Check backend API
curl https://yourdomain.com/api/v1/activities/destinations
curl https://yourdomain.com/docs

# Check frontend
curl https://yourdomain.com

# Check database
psql -U getyourguide_user -d getyourguide -h localhost -c "SELECT COUNT(*) FROM users;"
```

### 2. Create Admin Account

If you didn't run `init_db.py` with demo data:

```bash
cd /var/www/getyourguide/backend
source venv/bin/activate

python3 <<EOF
from app.database import SessionLocal
from app.models import User, UserRole
from app.core.security import get_password_hash

db = SessionLocal()
admin = User(
    email="admin@yourdomain.com",
    full_name="Admin User",
    password_hash=get_password_hash("StrongPassword123!"),
    role=UserRole.ADMIN,
    is_active=True
)
db.add(admin)
db.commit()
print(f"✅ Admin user created: {admin.email}")
db.close()
EOF
```

### 3. Performance Testing

```bash
# Install Apache Bench
sudo apt install -y apache2-utils

# Test API endpoint
ab -n 1000 -c 10 https://yourdomain.com/api/v1/activities/destinations

# Test frontend
ab -n 100 -c 10 https://yourdomain.com/
```

---

## Maintenance & Operations

### Monitoring

#### System Monitoring
```bash
# Install monitoring tools
sudo apt install -y htop iotop ncdu

# Monitor resources
htop           # CPU and memory
iotop          # Disk I/O
df -h          # Disk space
ncdu /var/www  # Disk usage analysis
```

#### Application Logs

```bash
# Backend logs (systemd)
sudo journalctl -u getyourguide-backend -f
sudo journalctl -u getyourguide-backend -n 100

# Frontend logs (PM2)
pm2 logs getyourguide-frontend
pm2 logs getyourguide-frontend --lines 100

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### Backup Strategy

#### Automated Database Backups

```bash
# Create backup script
sudo tee /usr/local/bin/backup-getyourguide.sh > /dev/null <<'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/getyourguide"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

mkdir -p $BACKUP_DIR

# Backup database
sudo -u postgres pg_dump getyourguide | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup application files (optional)
tar -czf $BACKUP_DIR/app_$DATE.tar.gz \
  --exclude='/var/www/getyourguide/backend/venv' \
  --exclude='/var/www/getyourguide/frontend/node_modules' \
  --exclude='/var/www/getyourguide/frontend/.next' \
  /var/www/getyourguide

# Keep only recent backups
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "app_*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "✅ Backup completed: $DATE"
EOF

sudo chmod +x /usr/local/bin/backup-getyourguide.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-getyourguide.sh") | crontab -

# Test backup script
/usr/local/bin/backup-getyourguide.sh

# List backups
ls -lh /var/backups/getyourguide/
```

#### Restore from Backup

```bash
# Stop services
sudo systemctl stop getyourguide-backend
pm2 stop getyourguide-frontend

# Restore database
gunzip < /var/backups/getyourguide/db_20250131_020000.sql.gz | \
  psql -U getyourguide_user -d getyourguide

# Restore application files (if needed)
cd /var/www
sudo tar -xzf /var/backups/getyourguide/app_20250131_020000.tar.gz

# Start services
sudo systemctl start getyourguide-backend
pm2 start getyourguide-frontend
```

### Updating Application

```bash
# 1. Backup before updating
/usr/local/bin/backup-getyourguide.sh

# 2. Pull latest changes
cd /var/www/getyourguide
git pull origin main

# 3. Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart getyourguide-backend

# 4. Update frontend
cd ../frontend
npm install
npm run build
pm2 restart getyourguide-frontend

# 5. Verify
curl https://yourdomain.com/docs
curl https://yourdomain.com/
```

### Database Optimization

```bash
# Connect to database
sudo -u postgres psql getyourguide

# Create performance indexes
CREATE INDEX IF NOT EXISTS idx_activities_slug ON activities(slug);
CREATE INDEX IF NOT EXISTS idx_activities_destination ON activities(destination_id);
CREATE INDEX IF NOT EXISTS idx_activities_vendor ON activities(vendor_id);
CREATE INDEX IF NOT EXISTS idx_bookings_user ON bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_bookings_activity ON bookings(activity_id);
CREATE INDEX IF NOT EXISTS idx_reviews_activity ON reviews(activity_id);
CREATE INDEX IF NOT EXISTS idx_cart_items_session ON cart_items(session_id);

# Analyze query performance
EXPLAIN ANALYZE SELECT * FROM activities WHERE destination_id = 1;

# Vacuum and analyze (maintenance)
VACUUM ANALYZE;
```

### Log Rotation

```bash
# Create log rotation config
sudo tee /etc/logrotate.d/getyourguide > /dev/null <<EOF
/var/log/getyourguide/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload getyourguide-backend > /dev/null 2>&1 || true
    endscript
}
EOF
```

### Security Checklist

- [ ] Changed all default passwords (admin, database)
- [ ] Generated strong SECRET_KEY (32+ character random hex)
- [ ] SSL/HTTPS enabled and working
- [ ] Firewall configured (UFW/AWS Security Groups)
- [ ] Disabled root SSH login (`PermitRootLogin no` in sshd_config)
- [ ] Setup fail2ban for brute force protection
- [ ] Regular security updates enabled (`unattended-upgrades`)
- [ ] Database user has minimum required permissions
- [ ] Environment variables secured (.env not in git)
- [ ] Automated backups configured and tested
- [ ] Monitoring and alerting in place
- [ ] CORS configured correctly for production domain
- [ ] Rate limiting configured (nginx/application level)

### Troubleshooting

#### Backend Not Starting

```bash
# Check logs
sudo journalctl -u getyourguide-backend -n 100

# Check if port 8000 is in use
sudo lsof -i :8000
sudo netstat -tulpn | grep 8000

# Test manually
cd /var/www/getyourguide/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Restart service
sudo systemctl restart getyourguide-backend
```

#### Frontend Not Starting

```bash
# Check PM2 logs
pm2 logs getyourguide-frontend --err
pm2 logs getyourguide-frontend --out

# Check process status
pm2 status

# Test manually
cd /var/www/getyourguide/frontend
npm start

# Restart
pm2 restart getyourguide-frontend
pm2 reload getyourguide-frontend
```

#### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U getyourguide_user -d getyourguide -h localhost

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Check access logs
sudo tail -f /var/log/nginx/access.log

# Restart nginx
sudo systemctl restart nginx

# Check if nginx is running
sudo systemctl status nginx
```

#### SSL Certificate Issues

```bash
# Check certificate expiration
sudo certbot certificates

# Manually renew
sudo certbot renew

# Force renewal (if close to expiry)
sudo certbot renew --force-renewal

# Test renewal process
sudo certbot renew --dry-run
```

#### High Memory Usage

```bash
# Check memory usage
free -h
htop

# Check which process is using memory
ps aux --sort=-%mem | head

# Restart services if needed
sudo systemctl restart getyourguide-backend
pm2 restart getyourguide-frontend

# Consider increasing swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### Disk Space Issues

```bash
# Check disk usage
df -h
ncdu /var/www

# Clean up logs
sudo journalctl --vacuum-time=7d
pm2 flush

# Clean package caches
sudo apt clean
sudo apt autoremove

# Clean old backups
sudo find /var/backups/getyourguide -mtime +30 -delete
```

---

## Support

For issues and questions:
1. Check application logs first
2. Review relevant troubleshooting section
3. Verify all services are running
4. Test database connectivity
5. Check firewall and network settings
6. Review environment variables

Common resources:
- **Backend API Docs**: https://yourdomain.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Next.js Documentation**: https://nextjs.org/docs
- **PostgreSQL Documentation**: https://www.postgresql.org/docs
- **Nginx Documentation**: https://nginx.org/en/docs
