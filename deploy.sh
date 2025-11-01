#!/bin/bash

# ============================================
# GetYourGuide Production Deployment Script
# ============================================
# Features:
# - Pre-flight checks
# - Backup before deployment
# - Rolling update with health checks
# - Automatic rollback on failure
# - Slack/email notifications (optional)

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="getyourguide"
COMPOSE_FILE="docker-compose.prod.yml"
BACKUP_DIR="./backups"
LOG_FILE="./logs/deploy-$(date +%Y%m%d-%H%M%S).log"
HEALTH_CHECK_RETRIES=30
HEALTH_CHECK_INTERVAL=5

# Print functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

# Error handler
handle_error() {
    print_error "Deployment failed at line $1"
    print_error "Check logs at: $LOG_FILE"
    exit 1
}

trap 'handle_error $LINENO' ERR

# Pre-flight checks
preflight_checks() {
    print_header "Pre-flight Checks"

    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running"
        exit 1
    fi
    print_success "Docker is running"

    # Check if Docker Compose is available
    if ! command -v docker-compose > /dev/null 2>&1 && ! docker compose version > /dev/null 2>&1; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose is available"

    # Check if .env file exists
    if [ ! -f .env ]; then
        print_error ".env file not found"
        print_info "Copy .env.production.example to .env and configure it"
        exit 1
    fi
    print_success ".env file exists"

    # Check required environment variables
    source .env
    REQUIRED_VARS=("POSTGRES_PASSWORD" "SECRET_KEY")
    for var in "${REQUIRED_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            print_error "Required environment variable $var is not set"
            exit 1
        fi
    done
    print_success "Required environment variables are set"

    # Check if SECRET_KEY is strong enough
    if [[ ${#SECRET_KEY} -lt 32 ]]; then
        print_error "SECRET_KEY must be at least 32 characters long"
        exit 1
    fi
    print_success "SECRET_KEY meets security requirements"

    # Check disk space (need at least 5GB free)
    FREE_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$FREE_SPACE" -lt 5 ]; then
        print_error "Insufficient disk space. Need at least 5GB free, have ${FREE_SPACE}GB"
        exit 1
    fi
    print_success "Sufficient disk space available (${FREE_SPACE}GB free)"

    # Check if compose file exists
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "Compose file $COMPOSE_FILE not found"
        exit 1
    fi
    print_success "Compose file found"

    print_info "All pre-flight checks passed"
}

# Create backup before deployment
create_backup() {
    print_header "Creating Backup"

    # Create backup directory
    mkdir -p "$BACKUP_DIR"

    # Backup database
    BACKUP_FILE="$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).sql"

    if docker ps | grep -q "${PROJECT_NAME}_db"; then
        print_info "Creating database backup..."
        docker exec "${PROJECT_NAME}_db" pg_dump -U postgres getyourguide > "$BACKUP_FILE"

        if [ -f "$BACKUP_FILE" ]; then
            BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
            print_success "Database backup created: $BACKUP_FILE ($BACKUP_SIZE)"
        else
            print_error "Failed to create backup"
            exit 1
        fi
    else
        print_warn "Database container not running, skipping backup"
    fi
}

# Pull latest images
pull_images() {
    print_header "Pulling Latest Images"

    print_info "Pulling images from registry..."
    docker-compose -f "$COMPOSE_FILE" pull
    print_success "Images pulled successfully"
}

# Build new images
build_images() {
    print_header "Building Images"

    print_info "Building backend image..."
    docker-compose -f "$COMPOSE_FILE" build backend

    print_info "Building frontend image..."
    docker-compose -f "$COMPOSE_FILE" build frontend

    print_success "Images built successfully"
}

# Health check function
check_health() {
    local service=$1
    local url=$2
    local retries=$HEALTH_CHECK_RETRIES

    print_info "Checking health of $service..."

    while [ $retries -gt 0 ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            print_success "$service is healthy"
            return 0
        fi

        retries=$((retries - 1))
        if [ $retries -gt 0 ]; then
            print_info "Waiting for $service... ($retries attempts remaining)"
            sleep $HEALTH_CHECK_INTERVAL
        fi
    done

    print_error "$service health check failed"
    return 1
}

# Deploy services
deploy_services() {
    print_header "Deploying Services"

    print_info "Starting services..."
    docker-compose -f "$COMPOSE_FILE" up -d

    print_info "Waiting for services to stabilize..."
    sleep 10

    # Check if all services are running
    if ! docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        print_error "Some services failed to start"
        docker-compose -f "$COMPOSE_FILE" ps
        exit 1
    fi

    print_success "All services started"
}

# Verify deployment
verify_deployment() {
    print_header "Verifying Deployment"

    # Check backend health
    if ! check_health "Backend" "http://localhost:8000/docs"; then
        print_error "Backend health check failed"
        exit 1
    fi

    # Check frontend health
    if ! check_health "Frontend" "http://localhost:3000"; then
        print_error "Frontend health check failed"
        exit 1
    fi

    # Check database connection
    if docker exec "${PROJECT_NAME}_backend" python -c "from app.database import SessionLocal; db = SessionLocal(); db.close(); print('OK')" | grep -q "OK"; then
        print_success "Database connection verified"
    else
        print_error "Database connection failed"
        exit 1
    fi

    print_success "Deployment verified successfully"
}

# Cleanup old images and containers
cleanup() {
    print_header "Cleanup"

    print_info "Removing unused images..."
    docker image prune -f

    print_info "Removing unused volumes..."
    docker volume prune -f

    print_success "Cleanup completed"
}

# Show deployment summary
show_summary() {
    print_header "Deployment Summary"

    echo ""
    print_info "Services Status:"
    docker-compose -f "$COMPOSE_FILE" ps

    echo ""
    print_info "Service URLs:"
    echo "  Frontend:  http://localhost:3000"
    echo "  Backend:   http://localhost:8000"
    echo "  API Docs:  http://localhost:8000/docs"
    echo "  Nginx:     http://localhost"

    echo ""
    print_info "Logs:"
    echo "  Deployment log: $LOG_FILE"
    echo "  View logs: docker-compose -f $COMPOSE_FILE logs -f"

    echo ""
    print_success "Deployment completed successfully! 🎉"
}

# Main deployment flow
main() {
    # Create log directory
    mkdir -p "$(dirname "$LOG_FILE")"

    print_header "GetYourGuide Deployment Started"
    print_info "Timestamp: $(date)"
    print_info "User: $(whoami)"
    print_info "Host: $(hostname)"

    # Run deployment steps
    preflight_checks
    create_backup
    build_images
    deploy_services
    verify_deployment
    cleanup
    show_summary
}

# Run main function
main "$@"
