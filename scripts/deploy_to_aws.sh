#!/bin/bash
set -e

# FindTravelMate AWS Deployment Script
# Based on successful deployment experience (November 2025)
# 
# This script automates the deployment workflow that was manually tested:
# 1. Create database backup
# 2. Transfer to AWS
# 3. Restore database
# 4. Restart services
# 5. Verify deployment

# Configuration
AWS_HOST="ec2-54-217-173-125.eu-west-1.compute.amazonaws.com"
AWS_USER="ubuntu"
PEM_FILE="ocrbot.pem"
LOCAL_DB_URL="postgresql://hongyusu@localhost:5432/findtravelmate"
AWS_DB_URL="postgresql://ubuntu:ubuntu123@localhost:5432/findtravelmate"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}🚀 FindTravelMate AWS Deployment${NC}"
    echo "=================================="
}

print_step() {
    echo -e "${BLUE}📍 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_prerequisites() {
    print_step "Checking prerequisites..."
    
    # Check if PEM file exists
    if [ ! -f "$PEM_FILE" ]; then
        print_error "PEM file not found: $PEM_FILE"
        exit 1
    fi
    
    # Check if DATABASE_URL is set for local
    if [ -z "$DATABASE_URL" ]; then
        print_warning "Setting DATABASE_URL for local database"
        export DATABASE_URL="$LOCAL_DB_URL"
    fi
    
    # Check if we can connect to local database
    if ! psql "$DATABASE_URL" -c "SELECT 1;" > /dev/null 2>&1; then
        print_error "Cannot connect to local database"
        exit 1
    fi
    
    # Check if we can SSH to AWS
    if ! ssh -i "$PEM_FILE" -o ConnectTimeout=10 "$AWS_USER@$AWS_HOST" "echo 'SSH test successful'" > /dev/null 2>&1; then
        print_error "Cannot SSH to AWS server"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

create_backup() {
    print_step "Creating database backup..."
    
    # Run backup script
    if ! python backend/backup_database.py; then
        print_error "Failed to create database backup"
        exit 1
    fi
    
    # Find the latest backup file
    BACKUP_FILE=$(ls -t backups/backup_*.sql | head -n1)
    if [ -z "$BACKUP_FILE" ]; then
        print_error "No backup file found"
        exit 1
    fi
    
    print_success "Backup created: $BACKUP_FILE"
}

transfer_backup() {
    print_step "Transferring backup to AWS..."
    
    if ! scp -i "$PEM_FILE" "$BACKUP_FILE" "$AWS_USER@$AWS_HOST:/home/ubuntu/"; then
        print_error "Failed to transfer backup file"
        exit 1
    fi
    
    BACKUP_FILENAME=$(basename "$BACKUP_FILE")
    print_success "Backup transferred: $BACKUP_FILENAME"
}

restore_database() {
    print_step "Restoring database on AWS..."
    
    # Create restoration script on AWS
    ssh -i "$PEM_FILE" "$AWS_USER@$AWS_HOST" "cat > restore_backup.sh << 'EOF'
#!/bin/bash
set -e

BACKUP_FILE=\"$BACKUP_FILENAME\"
export PGPASSWORD=ubuntu123

echo \"🗑️  Dropping existing database...\"
dropdb --host localhost --port 5432 --username ubuntu --if-exists findtravelmate 2>/dev/null || true

echo \"🆕 Creating fresh database...\"
createdb --host localhost --port 5432 --username ubuntu findtravelmate

echo \"📥 Restoring from backup...\"
psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate --file \"\$BACKUP_FILE\" --quiet

echo \"🔍 Verifying restoration...\"
echo \"Tables: \$(psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate --tuples-only -c 'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = \\'public\\';' | xargs)\"
echo \"Activities: \$(psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate --tuples-only -c 'SELECT COUNT(*) FROM activities;' | xargs)\"
echo \"Categories: \$(psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate --tuples-only -c 'SELECT COUNT(*) FROM categories;' | xargs)\"

echo \"✅ Database restoration completed\"
EOF"
    
    # Execute restoration script
    if ! ssh -i "$PEM_FILE" "$AWS_USER@$AWS_HOST" "chmod +x restore_backup.sh && ./restore_backup.sh"; then
        print_error "Failed to restore database"
        exit 1
    fi
    
    print_success "Database restoration completed"
}

restart_services() {
    print_step "Restarting AWS services..."
    
    # Restart backend service
    ssh -i "$PEM_FILE" "$AWS_USER@$AWS_HOST" "
        echo '🔄 Restarting backend service...'
        sudo systemctl restart findtravelmate-backend
        sleep 3
        
        echo '🔄 Restarting frontend service...'
        pm2 restart findtravelmate-frontend || pm2 start ecosystem.config.js
        sleep 5
    "
    
    print_success "Services restarted"
}

verify_deployment() {
    print_step "Verifying deployment..."
    
    # Check backend service status
    ssh -i "$PEM_FILE" "$AWS_USER@$AWS_HOST" "
        echo '🔍 Checking backend service...'
        if sudo systemctl is-active --quiet findtravelmate-backend; then
            echo '✅ Backend service is running'
        else
            echo '❌ Backend service is not running'
            exit 1
        fi
        
        echo '🔍 Checking frontend service...'
        if pm2 list | grep -q 'online.*findtravelmate-frontend'; then
            echo '✅ Frontend service is running'
        else
            echo '❌ Frontend service is not running'
            exit 1
        fi
        
        echo '🔍 Testing API endpoints...'
        if curl -s http://localhost:8000/api/v1/activities/categories | grep -q '\"name\"'; then
            echo '✅ Backend API is responding'
        else
            echo '❌ Backend API is not responding'
            exit 1
        fi
        
        echo '🔍 Testing frontend...'
        if curl -s http://localhost:3000 | grep -q 'FindTravelMate'; then
            echo '✅ Frontend is responding'
        else
            echo '❌ Frontend is not responding'
            exit 1
        fi
    "
    
    # Test external access
    print_step "Testing external access..."
    
    if curl -s "http://$AWS_HOST:8000/api/v1/activities/categories" | grep -q '"name"'; then
        print_success "Backend API accessible externally"
    else
        print_error "Backend API not accessible externally"
        exit 1
    fi
    
    if curl -s "http://$AWS_HOST:3000" | grep -q 'FindTravelMate'; then
        print_success "Frontend accessible externally"
    else
        print_error "Frontend not accessible externally"
        exit 1
    fi
    
    print_success "Deployment verification completed"
}

cleanup() {
    print_step "Cleaning up..."
    
    # Remove backup file from AWS
    ssh -i "$PEM_FILE" "$AWS_USER@$AWS_HOST" "rm -f $BACKUP_FILENAME restore_backup.sh"
    
    print_success "Cleanup completed"
}

show_summary() {
    echo ""
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
    echo ""
    echo "📱 Frontend: http://$AWS_HOST:3000"
    echo "🔧 Backend API: http://$AWS_HOST:8000/api/v1"
    echo "📚 API Docs: http://$AWS_HOST:8000/api/v1/docs"
    echo ""
    echo "👤 Demo accounts:"
    echo "   Customer: customer@example.com / customer123"
    echo "   Admin: admin@findtravelmate.com / admin123"
    echo "   Vendor: vendor1@example.com / vendor123"
    echo ""
    echo "🔧 Management commands:"
    echo "   Backend: ssh -i $PEM_FILE $AWS_USER@$AWS_HOST 'sudo systemctl status findtravelmate-backend'"
    echo "   Frontend: ssh -i $PEM_FILE $AWS_USER@$AWS_HOST 'pm2 status'"
}

# Main execution
main() {
    print_header
    
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "Usage: $0 [--dry-run]"
        echo ""
        echo "This script automates the FindTravelMate AWS deployment process:"
        echo "1. Creates a backup of the local database"
        echo "2. Transfers the backup to AWS server"
        echo "3. Restores the database on AWS"
        echo "4. Restarts backend and frontend services"
        echo "5. Verifies that everything is working correctly"
        echo ""
        echo "Options:"
        echo "  --dry-run    Show what would be done without executing"
        echo "  --help       Show this help message"
        exit 0
    fi
    
    if [ "$1" = "--dry-run" ]; then
        echo "🔍 DRY RUN MODE - showing what would be done:"
        echo "1. Check prerequisites (PEM file, database connection, SSH access)"
        echo "2. Create database backup using backend/backup_database.py"
        echo "3. Transfer backup to AWS server via SCP"
        echo "4. Restore database on AWS (drop, create, restore)"
        echo "5. Restart backend and frontend services"
        echo "6. Verify external access to both services"
        echo "7. Clean up temporary files"
        exit 0
    fi
    
    # Ask for confirmation
    echo -e "${YELLOW}⚠️  This will replace the AWS database with local data. Continue? (y/N)${NC}"
    read -r response
    if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
        echo "Deployment cancelled"
        exit 0
    fi
    
    # Execute deployment steps
    check_prerequisites
    create_backup
    transfer_backup
    restore_database
    restart_services
    verify_deployment
    cleanup
    show_summary
}

# Execute main function with all arguments
main "$@"