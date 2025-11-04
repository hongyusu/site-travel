# FindTravelMate Deployment Scripts

This directory contains scripts for managing FindTravelMate deployments, based on successful AWS deployment experience (November 2025).

## Scripts Overview

### 🚀 `deploy_to_aws.sh`
**Main AWS deployment automation script**

Automates the complete deployment workflow:
1. Creates database backup from local
2. Transfers backup to AWS server
3. Restores database on AWS
4. Restarts all services
5. Verifies deployment functionality

```bash
# Full deployment
./scripts/deploy_to_aws.sh

# See what would be done
./scripts/deploy_to_aws.sh --dry-run

# Get help
./scripts/deploy_to_aws.sh --help
```

**Requirements:**
- `ocrbot.pem` file in project root
- Local database running and accessible
- SSH access to AWS server

### 🔍 `verify_deployment.py`
**Deployment verification and comparison tool**

Tests deployments and compares data consistency between environments.

```bash
# Verify local deployment
python scripts/verify_deployment.py --local

# Verify AWS deployment  
python scripts/verify_deployment.py --aws

# Compare local vs AWS data
python scripts/verify_deployment.py --compare

# Run all verifications
python scripts/verify_deployment.py --all
```

**Features:**
- Database connectivity tests
- API endpoint verification
- Frontend accessibility checks
- Data consistency comparison
- SSH connectivity validation (AWS)

## Backend Scripts

### 📦 `backend/backup_database.py`
**Creates timestamped database backups**

```bash
export DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"
python backend/backup_database.py
```

**Output:** `backups/backup_YYYY-MM-DD_HH-MM-SS.sql`

### 📥 `backend/restore_database.py` 
**Restores database from backup files**

```bash
# Local restoration
export DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"
python backend/restore_database.py backup_file.sql

# AWS restoration (with guidance)
python backend/restore_database.py backup_file.sql --aws

# List available backups
python backend/restore_database.py --list
```

**Features:**
- Connection testing
- Database existence checks
- Comprehensive verification
- AWS-specific guidance

### 🛠️ `backend/initialize_database.py`
**Initialize fresh database from backup**

```bash
python backend/initialize_database.py backup_file.sql
python backend/initialize_database.py --list
```

## Usage Workflows

### 🔄 Complete AWS Deployment
```bash
# 1. Ensure local development is working
python scripts/verify_deployment.py --local

# 2. Deploy to AWS (automated)
./scripts/deploy_to_aws.sh

# 3. Verify AWS deployment
python scripts/verify_deployment.py --aws

# 4. Compare data consistency
python scripts/verify_deployment.py --compare
```

### 🔧 Manual Database Sync
```bash
# 1. Create backup
export DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"
python backend/backup_database.py

# 2. Copy to AWS
scp -i ocrbot.pem backup_*.sql ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com:/home/ubuntu/

# 3. Restore on AWS
ssh -i ocrbot.pem ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com
export DATABASE_URL="postgresql://ubuntu:ubuntu123@localhost:5432/findtravelmate"
python restore_database.py backup_*.sql --aws
```

### 🩺 Health Checks
```bash
# Quick verification
python scripts/verify_deployment.py --all

# Detailed database stats
export DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"
python backend/restore_database.py --list
```

## Configuration

### Environment Variables
- **Local**: `DATABASE_URL="postgresql://hongyusu@localhost:5432/findtravelmate"`
- **AWS**: `DATABASE_URL="postgresql://ubuntu:ubuntu123@localhost:5432/findtravelmate"`

### AWS Server Details
- **Host**: `ec2-54-217-173-125.eu-west-1.compute.amazonaws.com`
- **User**: `ubuntu`
- **PEM File**: `ocrbot.pem` (must be in project root)
- **Frontend**: http://54.217.173.125:3000
- **Backend**: http://54.217.173.125:8000/api/v1

### Service Management (AWS)
```bash
# Backend service
sudo systemctl status findtravelmate-backend
sudo systemctl restart findtravelmate-backend

# Frontend service
pm2 status
pm2 restart findtravelmate-frontend

# Database service
sudo systemctl status postgresql
```

## Troubleshooting

### Common Issues

#### 1. Permission Denied on Scripts
```bash
chmod +x scripts/deploy_to_aws.sh
```

#### 2. Database Connection Errors
```bash
# Check if DATABASE_URL is set correctly
echo $DATABASE_URL

# Test connection manually
psql $DATABASE_URL -c "SELECT version();"
```

#### 3. SSH Connection Issues
```bash
# Test SSH connectivity
ssh -i ocrbot.pem ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com "echo 'test'"

# Check PEM file permissions
chmod 400 ocrbot.pem
```

#### 4. Service Not Starting
```bash
# Check backend logs
ssh -i ocrbot.pem ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com "sudo journalctl -u findtravelmate-backend -n 20"

# Check frontend logs
ssh -i ocrbot.pem ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com "pm2 logs findtravelmate-frontend"
```

## Best Practices

1. **Always verify before deployment**: Run `--dry-run` first
2. **Test connectivity**: Use verification scripts before and after deployment
3. **Compare data**: Always check data consistency between environments
4. **Backup first**: Create fresh backups before any major changes
5. **Monitor logs**: Check service logs after deployment

## Expected Data (November 2025)
- **Categories**: 10 (Tours, Food & Drink, Museums & Culture, etc.)
- **Activities**: 21 (Stockholm tours, Louvre visits, Chinese experiences, etc.)
- **Destinations**: 10+ cities worldwide
- **Users**: 20+ (admin, customers, vendors)

## Support

For issues or questions:
1. Check the main [SETUP_GUIDE.md](../SETUP_GUIDE.md)
2. Run verification scripts for diagnostics
3. Check service logs on AWS server
4. Verify database connectivity and data consistency