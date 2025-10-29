# Docker Quick Start

Get your GetYourGuide clone running with Docker in 5 minutes!

## Prerequisites

```bash
# Check Docker is installed
docker --version
docker-compose --version
```

## 1. Setup Environment

```bash
# Copy environment template
cp .env.docker.example .env

# Generate secure keys
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
echo "POSTGRES_PASSWORD=$(openssl rand -base64 16)" >> .env
```

## 2. Launch Application

```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy (30-60 seconds)
docker-compose -f docker-compose.prod.yml ps
```

## 3. Initialize Database

```bash
# Run database setup
chmod +x docker-init-db.sh
./docker-init-db.sh
```

## 4. Create Admin User

```bash
docker-compose -f docker-compose.prod.yml exec backend python -c "
from app.database import SessionLocal
from app.models import User, UserRole
from app.core.security import get_password_hash

db = SessionLocal()
admin = User(
    email='admin@example.com',
    full_name='Admin',
    password_hash=get_password_hash('admin123'),
    role=UserRole.ADMIN,
    is_active=True
)
db.add(admin)
db.commit()
print('✅ Admin created')
db.close()
"
```

## 5. Access Application

Open your browser:
- **Application**: http://localhost
- **API Docs**: http://localhost/docs
- **Admin Login**: admin@example.com / admin123

## Troubleshooting

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Stop everything
docker-compose -f docker-compose.prod.yml down

# Start fresh (DELETES DATA!)
docker-compose -f docker-compose.prod.yml down -v
```

## Next Steps

See [DOCKER-DEPLOYMENT.md](DOCKER-DEPLOYMENT.md) for:
- Production configuration
- SSL setup
- Backup strategies
- Monitoring
- Scaling
