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
EC2_HOST="ec2-54-78-136-48.eu-west-1.compute.amazonaws.com"
EC2_USER="ubuntu"
DEPLOY_DIR="/home/ubuntu/getyourguide"

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

# Phase 1: Server Preparation
prepare_server() {
    print_header "Phase 1: Preparing EC2 Server"

    print_info "Installing system updates..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'EOF'
        sudo apt-get update
        sudo apt-get upgrade -y
EOF

    print_info "Installing Docker..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'EOF'
        # Install Docker
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker ubuntu
        rm get-docker.sh

        # Install Docker Compose
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose

        # Verify installations
        docker --version
        docker-compose --version
EOF

    print_info "Configuring firewall..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'EOF'
        sudo ufw allow 22/tcp
        sudo ufw allow 80/tcp
        sudo ufw allow 443/tcp
        sudo ufw allow 3000/tcp
        sudo ufw allow 8000/tcp
        sudo ufw --force enable
        sudo ufw status
EOF

    print_success "Server preparation complete"
}

# Phase 2: Code Deployment
deploy_code() {
    print_header "Phase 2: Deploying Code"

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
        -e "ssh -i \"$SSH_KEY\"" \
        . "$EC2_USER@$EC2_HOST:$DEPLOY_DIR/"

    print_success "Code deployment complete"
}

# Phase 3: Environment Configuration
configure_environment() {
    print_header "Phase 3: Configuring Environment"

    print_info "Generating production secrets..."
    SECRET_KEY=$(openssl rand -hex 32)
    DB_PASSWORD=$(openssl rand -base64 24)

    print_info "Creating .env file on server..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR

        # Create .env from template
        cp .env.production.example .env

        # Set secrets
        echo "SECRET_KEY=$SECRET_KEY" >> .env
        echo "POSTGRES_PASSWORD=$DB_PASSWORD" >> .env

        # Set production values
        sed -i 's/PYTHON_ENV=.*/PYTHON_ENV=production/' .env
        sed -i 's/LOG_LEVEL=.*/LOG_LEVEL=INFO/' .env
        sed -i 's/NEXT_PUBLIC_API_URL=.*/NEXT_PUBLIC_API_URL=http:\/\/54.78.136.48:8000/' .env
        sed -i "s|CORS_ORIGINS=.*|CORS_ORIGINS='[\"http://54.78.136.48:3000\",\"http://54.78.136.48\"]'|" .env
        sed -i "s|DATABASE_URL=.*|DATABASE_URL=postgresql://postgres:$DB_PASSWORD@postgres:5432/getyourguide|" .env

        # Make scripts executable
        chmod +x deploy.sh backup.sh backend/docker-entrypoint.sh docker-init-db.sh

        echo "✅ Environment configured"
EOF

    print_success "Environment configuration complete"
}

# Phase 4: Docker Deployment
deploy_docker() {
    print_header "Phase 4: Building and Starting Docker Containers"

    print_info "Building Docker images..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR
        docker-compose -f docker-compose.prod.yml build
EOF

    print_info "Starting services..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR
        docker-compose -f docker-compose.prod.yml up -d
EOF

    print_info "Waiting for services to start..."
    sleep 30

    print_info "Initializing database..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR
        ./docker-init-db.sh
EOF

    print_success "Docker deployment complete"
}

# Phase 5: Verification
verify_deployment() {
    print_header "Phase 5: Verifying Deployment"

    print_info "Checking container status..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR
        docker-compose -f docker-compose.prod.yml ps
EOF

    print_info "Testing health endpoints..."
    sleep 10

    # Test backend
    if curl -sf http://54.78.136.48:8000/docs > /dev/null; then
        print_success "Backend is healthy"
    else
        print_error "Backend health check failed"
    fi

    # Test frontend
    if curl -sf http://54.78.136.48:3000 > /dev/null; then
        print_success "Frontend is healthy"
    else
        print_error "Frontend health check failed"
    fi

    print_success "Verification complete"
}

# Phase 6: Post-Deployment
post_deployment() {
    print_header "Phase 6: Post-Deployment Configuration"

    print_info "Setting up automated backups..."
    ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << EOF
        cd $DEPLOY_DIR

        # Add backup cron job (daily at 2 AM)
        (crontab -l 2>/dev/null; echo "0 2 * * * cd $DEPLOY_DIR && ./backup.sh") | crontab -

        echo "✅ Backup cron job configured"
EOF

    print_success "Post-deployment configuration complete"
}

# Show deployment summary
show_summary() {
    print_header "Deployment Summary"

    echo ""
    print_info "🎉 Deployment completed successfully!"
    echo ""
    print_info "Access URLs:"
    echo "  Frontend:  http://54.78.136.48:3000"
    echo "  Backend:   http://54.78.136.48:8000"
    echo "  API Docs:  http://54.78.136.48:8000/docs"
    echo ""
    print_info "Demo Accounts:"
    echo "  Admin:    admin@getyourguide.com / admin123"
    echo "  Customer: customer@example.com / customer123"
    echo "  Vendor:   vendor1@example.com / vendor123"
    echo ""
    print_info "SSH Access:"
    echo "  ssh -i ocrbot.pem ubuntu@ec2-54-78-136-48.eu-west-1.compute.amazonaws.com"
    echo ""
    print_info "Management Commands (on server):"
    echo "  cd $DEPLOY_DIR"
    echo "  docker-compose -f docker-compose.prod.yml logs -f"
    echo "  docker-compose -f docker-compose.prod.yml restart"
    echo "  ./backup.sh"
    echo ""
}

# Main execution
main() {
    print_header "AWS EC2 Deployment Started"
    print_info "Target: $EC2_HOST"
    print_info "Timestamp: $(date)"
    echo ""

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
