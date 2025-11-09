#!/bin/bash

# ============================================
# AWS EC2 Deployment Script
# ============================================
# Automated deployment to EC2 instance
# Usage: ./deploy-aws.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SSH_KEY="$SCRIPT_DIR/ocrbot.pem"
EC2_HOST="ec2-54-217-173-125.eu-west-1.compute.amazonaws.com"
EC2_USER="ubuntu"
DEPLOY_DIR="/home/ubuntu/findtravelmate"

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Phase 1: Stop Current Services and Backup
stop_current_services() {
    print_header "Phase 1: Stopping Current Services and Creating Backup"

    print_info "Stopping current manual services..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'EOF'
        # Stop any running Node.js processes
        pkill -f "npm\|node\|next" || true
        
        # Stop any Python/uvicorn processes
        pkill -f "uvicorn\|python.*app" || true
        
        # Stop nginx if running
        sudo systemctl stop nginx || true
        
        # Stop PostgreSQL if running locally
        sudo systemctl stop postgresql || true
        
        # Stop Redis if running locally
        sudo systemctl stop redis-server || true
        
        echo "✅ Current services stopped"
EOF

    print_info "Creating database backup..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'EOF'
        # Create backups directory
        mkdir -p /home/ubuntu/backups
        
        # Backup database if it exists
        if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw findtravelmate; then
            sudo -u postgres pg_dump findtravelmate > /home/ubuntu/backups/findtravelmate_pre_docker_$(date +%Y%m%d_%H%M%S).sql
            echo "✅ Database backup created"
        else
            echo "ℹ️ No existing database found to backup"
        fi
EOF

    print_success "Current services stopped and backup completed"
}

# Phase 2: Server Preparation  
prepare_server() {
    print_header "Phase 2: Preparing EC2 Server for Docker"

    print_info "Installing system updates..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'EOF'
        sudo apt-get update
        sudo apt-get upgrade -y
EOF

    print_info "Installing Docker if not present..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'EOF'
        # Check if Docker is already installed
        if ! command -v docker &> /dev/null; then
            # Install Docker
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker ubuntu
            rm get-docker.sh
            
            # Install Docker Compose
            sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            sudo chmod +x /usr/local/bin/docker-compose
            
            echo "✅ Docker installed"
        else
            echo "ℹ️ Docker already installed"
        fi
        
        # Verify installations
        docker --version
        docker-compose --version
EOF

    print_info "Configuring firewall..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'EOF'
        sudo ufw allow 22/tcp
        sudo ufw allow 80/tcp
        sudo ufw allow 443/tcp
        sudo ufw --force enable
        sudo ufw status
EOF

    print_success "Server preparation complete"
}

# Phase 3: Code Deployment
deploy_code() {
    print_header "Phase 3: Deploying Code"

    print_info "Creating deployment directory..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" "mkdir -p $DEPLOY_DIR"

    print_info "Transferring files to EC2..."
    rsync -avz --exclude 'node_modules' \
        --exclude '.next' \
        --exclude '__pycache__' \
        --exclude '*.pyc' \
        --exclude '.git' \
        --exclude 'venv' \
        --exclude '.env' \
        --exclude 'logs' \
        --exclude 'backups' \
        --exclude 'keys' \
        -e "ssh -i \"$SSH_KEY\"" \
        . "$EC2_USER@$EC2_HOST:$DEPLOY_DIR/"

    print_success "Code deployment complete"
}

# Phase 4: Environment Configuration
configure_environment() {
    print_header "Phase 4: Configuring Environment"

    print_info "Generating production secrets..."
    SECRET_KEY=$(openssl rand -hex 32)
    DB_PASSWORD=$(openssl rand -base64 24)

    print_info "Creating .env file on server..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR

        # Create .env from template
        cp .env.production .env

        # Replace placeholders with actual values
        sed -i "s/CHANGE_ME_IN_DEPLOYMENT/$SECRET_KEY/g" .env
        sed -i "s/YOUR_EC2_IP/54.217.173.125/g" .env
        
        # Set database password
        sed -i "s/POSTGRES_PASSWORD=CHANGE_ME_IN_DEPLOYMENT/POSTGRES_PASSWORD=$DB_PASSWORD/" .env
        
        # Update CORS origins to use actual IP
        sed -i 's|CORS_ORIGINS=\["http://YOUR_EC2_IP", "http://YOUR_EC2_IP:3000"\]|CORS_ORIGINS=["http://54.217.173.125", "http://54.217.173.125:3000"]|' .env

        # Make scripts executable if they exist
        find . -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
        
        # Make docker entrypoint executable
        chmod +x backend/docker-entrypoint.sh 2>/dev/null || true

        echo "✅ Environment configured"
EOF

    print_success "Environment configuration complete"
}

# Phase 5: Docker Deployment
deploy_docker() {
    print_header "Phase 5: Building and Starting Docker Containers"

    print_info "Stopping any existing containers..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR
        docker-compose down 2>/dev/null || true
        docker system prune -f 2>/dev/null || true
EOF

    print_info "Building Docker images..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR
        docker-compose build --no-cache
EOF

    print_info "Starting services..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR
        docker-compose up -d
EOF

    print_info "Waiting for services to start..."
    sleep 60

    print_info "Checking service health..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR
        docker-compose ps
        docker-compose logs --tail=20
EOF

    print_success "Docker deployment complete"
}

# Phase 6: Verification
verify_deployment() {
    print_header "Phase 6: Verifying Deployment"

    print_info "Checking container status..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR
        docker-compose ps
        docker-compose logs backend --tail=10
        docker-compose logs frontend --tail=10
EOF

    print_info "Testing health endpoints..."
    sleep 15

    # Test nginx health endpoint
    if curl -sf http://54.217.173.125/health > /dev/null; then
        print_success "Nginx is healthy"
    else
        print_error "Nginx health check failed"
    fi

    # Test backend API
    if curl -sf http://54.217.173.125/api/v1/activities/categories > /dev/null; then
        print_success "Backend API is healthy"
    else
        print_error "Backend API health check failed"
    fi

    # Test frontend
    if curl -sf http://54.217.173.125 > /dev/null; then
        print_success "Frontend is healthy"
    else
        print_error "Frontend health check failed"
    fi

    print_success "Verification complete"
}

# Phase 7: Post-Deployment
post_deployment() {
    print_header "Phase 7: Post-Deployment Configuration"

    print_info "Setting up automated backups..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR

        # Create a simple backup script for Docker
        cat > docker-backup.sh << 'BACKUP_EOF'
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/backups"
mkdir -p \$BACKUP_DIR

# Backup database from Docker container
docker-compose exec -T postgres pg_dump -U postgres findtravelmate > \$BACKUP_DIR/findtravelmate_\$DATE.sql

# Keep only last 7 backups
ls -t \$BACKUP_DIR/findtravelmate_*.sql | tail -n +8 | xargs rm -f

echo "✅ Database backup completed: findtravelmate_\$DATE.sql"
BACKUP_EOF

        chmod +x docker-backup.sh

        # Add backup cron job (daily at 2 AM)
        (crontab -l 2>/dev/null | grep -v docker-backup.sh; echo "0 2 * * * cd $DEPLOY_DIR && ./docker-backup.sh") | crontab -

        echo "✅ Docker backup cron job configured"
EOF

    print_success "Post-deployment configuration complete"
}

# Show deployment summary
show_summary() {
    print_header "Deployment Summary"

    echo ""
    print_info "🎉 Docker deployment completed successfully!"
    echo ""
    print_info "Access URLs:"
    echo "  Application: http://54.217.173.125"
    echo "  Backend API: http://54.217.173.125/api/v1"
    echo "  API Docs:    http://54.217.173.125/docs"
    echo "  Health:      http://54.217.173.125/health"
    echo ""
    print_info "Demo Accounts:"
    echo "  Admin:    admin@findtravelmate.com / admin123"
    echo "  Customer: customer@example.com / customer123"
    echo "  Vendor:   vendor1@example.com / vendor123"  
    echo ""
    print_info "SSH Access:"
    echo "  ssh -i ocrbot.pem ubuntu@ec2-54-217-173-125.eu-west-1.compute.amazonaws.com"
    echo ""
    print_info "Docker Management Commands (on server):"
    echo "  cd $DEPLOY_DIR"
    echo "  docker-compose ps              # Check container status"
    echo "  docker-compose logs -f         # View logs"
    echo "  docker-compose restart         # Restart all services"
    echo "  docker-compose down && docker-compose up -d  # Full restart"
    echo "  ./docker-backup.sh             # Manual backup"
    echo ""
}

# Main execution
main() {
    print_header "AWS EC2 Docker Deployment Started"
    print_info "Target: $EC2_HOST"
    print_info "Timestamp: $(date)"
    echo ""

    stop_current_services
    prepare_server
    deploy_code
    configure_environment
    deploy_docker
    verify_deployment
    post_deployment
    show_summary
}

# Run deployment
main "$@"
