#!/bin/bash
set -e

echo "🚀 Starting FindTravelMate Backend..."

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse DATABASE_URL to extract connection details
parse_database_url() {
    if [[ $DATABASE_URL =~ postgresql://([^:]+):([^@]+)@([^:]+):([^/]+)/(.+) ]]; then
        DB_USER="${BASH_REMATCH[1]}"
        DB_PASS="${BASH_REMATCH[2]}"
        DB_HOST="${BASH_REMATCH[3]}"
        DB_PORT="${BASH_REMATCH[4]}"
        DB_NAME="${BASH_REMATCH[5]}"
    else
        print_error "Failed to parse DATABASE_URL"
        exit 1
    fi
}

# Wait for database to be ready
wait_for_db() {
    print_info "Waiting for PostgreSQL to be ready..."

    parse_database_url

    MAX_RETRIES=30
    RETRY_COUNT=0

    until PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
        RETRY_COUNT=$((RETRY_COUNT + 1))

        if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
            print_error "Database is not available after ${MAX_RETRIES} attempts"
            exit 1
        fi

        print_warn "Database not ready yet (attempt $RETRY_COUNT/$MAX_RETRIES). Waiting 2 seconds..."
        sleep 2
    done

    print_info "✅ PostgreSQL is ready!"
}

# Check if database is initialized
check_db_initialized() {
    print_info "Checking if database is initialized..."

    parse_database_url

    # Check if users table exists
    TABLE_EXISTS=$(PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tAc \
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users');")

    if [ "$TABLE_EXISTS" = "t" ]; then
        print_info "✅ Database is already initialized"
        return 0
    else
        print_warn "Database is not initialized"
        return 1
    fi
}

# Initialize database with demo data
initialize_database() {
    print_info "Initializing database with schema and demo data..."

    if [ -f "init_db.py" ]; then
        python init_db.py
        if [ $? -eq 0 ]; then
            print_info "✅ Database initialized successfully!"
        else
            print_error "Failed to initialize database"
            exit 1
        fi
    else
        print_warn "init_db.py not found, skipping initialization"
    fi
}

# Run database migrations (if using Alembic)
run_migrations() {
    if [ -d "alembic" ] && [ -f "alembic.ini" ]; then
        print_info "Running database migrations..."
        alembic upgrade head
        if [ $? -eq 0 ]; then
            print_info "✅ Migrations completed successfully!"
        else
            print_error "Migrations failed"
            exit 1
        fi
    fi
}

# Validate environment variables
validate_env() {
    print_info "Validating environment variables..."

    MISSING_VARS=()

    [ -z "$DATABASE_URL" ] && MISSING_VARS+=("DATABASE_URL")
    [ -z "$SECRET_KEY" ] && MISSING_VARS+=("SECRET_KEY")
    [ -z "$ALGORITHM" ] && MISSING_VARS+=("ALGORITHM")

    if [ ${#MISSING_VARS[@]} -gt 0 ]; then
        print_error "Missing required environment variables: ${MISSING_VARS[*]}"
        exit 1
    fi

    # Warn if using default/insecure values
    if [[ "$SECRET_KEY" == *"your-secret-key"* ]] || [[ "$SECRET_KEY" == *"changeme"* ]]; then
        print_warn "⚠️  SECRET_KEY appears to be a default value. Please change it in production!"
    fi

    print_info "✅ Environment variables validated"
}

# Health check endpoint test
test_health() {
    print_info "Testing application health..."

    # Give the app a moment to start
    sleep 3

    HEALTH_URL="http://localhost:8000/docs"
    MAX_RETRIES=10
    RETRY_COUNT=0

    until curl -sf "$HEALTH_URL" > /dev/null 2>&1; do
        RETRY_COUNT=$((RETRY_COUNT + 1))

        if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
            print_warn "Health check endpoint not responding after ${MAX_RETRIES} attempts"
            break
        fi

        sleep 2
    done

    if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
        print_info "✅ Application is healthy!"
    fi
}

# Graceful shutdown handler
shutdown() {
    print_info "Received shutdown signal, gracefully stopping..."
    # Add any cleanup tasks here
    exit 0
}

# Trap SIGTERM and SIGINT
trap shutdown SIGTERM SIGINT

# Main execution
main() {
    print_info "========================================"
    print_info "  FindTravelMate Backend Entrypoint"
    print_info "========================================"

    # Validate environment
    validate_env

    # Wait for database
    wait_for_db

    # Check if we should initialize the database
    if [ "$AUTO_INIT_DB" = "true" ] || [ "$AUTO_INIT_DB" = "1" ]; then
        if ! check_db_initialized; then
            initialize_database
        fi
    else
        check_db_initialized || print_warn "Database not initialized. Set AUTO_INIT_DB=true to auto-initialize."
    fi

    # Run migrations if available
    run_migrations

    print_info "========================================"
    print_info "Starting Uvicorn server..."
    print_info "========================================"

    # Execute the main command (passed as arguments to this script)
    exec "$@"
}

# Run main function
main "$@"
