#!/bin/bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

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

wait_for_db() {
    print_info "Waiting for PostgreSQL..."
    parse_database_url
    for i in $(seq 1 30); do
        if PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; then
            print_info "PostgreSQL is ready."
            return 0
        fi
        print_warn "Attempt $i/30..."
        sleep 2
    done
    print_error "Database not available after 30 attempts"
    exit 1
}

db_has_data() {
    parse_database_url
    TABLE_EXISTS=$(PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tAc \
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users');" 2>/dev/null)
    if [ "$TABLE_EXISTS" != "t" ]; then
        return 1  # no tables
    fi
    USER_COUNT=$(PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tAc \
        "SELECT count(*) FROM users;" 2>/dev/null || echo "0")
    [ "$USER_COUNT" -gt "0" ] 2>/dev/null
}

initialize_database() {
    print_info "Database is empty — initializing..."

    # Step 1: Create tables via SQLAlchemy models
    if [ -f "init_db.py" ]; then
        print_info "Creating schema..."
        python init_db.py
    fi

    # Step 2: Restore demo data from backup if available
    BACKUP_FILE="/backups/backup_2026-04-14_polished.sql"
    if [ -f "$BACKUP_FILE" ]; then
        print_info "Restoring demo data from backup..."
        parse_database_url
        PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f "$BACKUP_FILE" --quiet 2>/dev/null
        if [ $? -eq 0 ]; then
            ACTIVITY_COUNT=$(PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tAc \
                "SELECT count(*) FROM activities;" 2>/dev/null || echo "0")
            print_info "Restored: ${ACTIVITY_COUNT} activities loaded."
        else
            print_warn "Backup restore had warnings (this is usually fine)."
        fi
    else
        print_warn "No backup file found at $BACKUP_FILE — database has schema but no demo data."
    fi
}

main() {
    print_info "========================================"
    print_info "  FindTravelMate Backend Entrypoint"
    print_info "========================================"

    # Validate required env vars
    [ -z "$DATABASE_URL" ] && print_error "DATABASE_URL not set" && exit 1
    [ -z "$SECRET_KEY" ] && print_error "SECRET_KEY not set" && exit 1

    # Wait for database
    wait_for_db

    # Auto-initialize if database is empty
    if ! db_has_data; then
        initialize_database
    else
        print_info "Database already has data — skipping initialization."
    fi

    print_info "Starting Uvicorn..."
    exec "$@"
}

trap 'echo "Shutting down..."; exit 0' SIGTERM SIGINT
main "$@"
