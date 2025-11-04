#!/bin/bash

# ============================================
# GetYourGuide Database Backup Script
# ============================================
# Features:
# - Full PostgreSQL database backup
# - Compressed archives
# - Automatic retention management
# - Upload to S3 (optional)
# - Email notifications (optional)
# - Restore functionality

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="findtravelmate"
DB_CONTAINER="${PROJECT_NAME}_db"
BACKUP_DIR="./backups"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup-$TIMESTAMP.sql"
COMPRESSED_FILE="$BACKUP_FILE.gz"
LOG_FILE="./logs/backup-$TIMESTAMP.log"

# Optional S3 configuration
S3_ENABLED="${BACKUP_S3_ENABLED:-false}"
S3_BUCKET="${BACKUP_S3_BUCKET:-}"
AWS_REGION="${AWS_REGION:-us-east-1}"

# Print functions
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
    print_error "Backup failed at line $1"
    print_error "Check logs at: $LOG_FILE"
    exit 1
}

trap 'handle_error $LINENO' ERR

# Check if database container is running
check_container() {
    if ! docker ps | grep -q "$DB_CONTAINER"; then
        print_error "Database container $DB_CONTAINER is not running"
        exit 1
    fi
    print_success "Database container is running"
}

# Create backup directory
create_backup_dir() {
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$(dirname "$LOG_FILE")"
    print_success "Backup directory created"
}

# Create database backup
create_backup() {
    print_info "Creating database backup..."

    # Get database credentials from environment
    source .env 2>/dev/null || true

    # Create backup
    docker exec "$DB_CONTAINER" pg_dump -U postgres -Fc findtravelmate > "$BACKUP_FILE"

    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Failed to create backup file"
        exit 1
    fi

    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    print_success "Backup created: $BACKUP_FILE ($BACKUP_SIZE)"
}

# Compress backup
compress_backup() {
    print_info "Compressing backup..."

    gzip "$BACKUP_FILE"

    if [ ! -f "$COMPRESSED_FILE" ]; then
        print_error "Failed to compress backup"
        exit 1
    fi

    COMPRESSED_SIZE=$(du -h "$COMPRESSED_FILE" | cut -f1)
    print_success "Backup compressed: $COMPRESSED_FILE ($COMPRESSED_SIZE)"
}

# Upload to S3 (optional)
upload_to_s3() {
    if [ "$S3_ENABLED" != "true" ]; then
        print_info "S3 upload disabled, skipping"
        return 0
    fi

    if [ -z "$S3_BUCKET" ]; then
        print_warn "S3_BUCKET not configured, skipping upload"
        return 0
    fi

    print_info "Uploading to S3..."

    if command -v aws > /dev/null 2>&1; then
        aws s3 cp "$COMPRESSED_FILE" "s3://$S3_BUCKET/backups/$(basename "$COMPRESSED_FILE")" \
            --region "$AWS_REGION"

        print_success "Backup uploaded to S3: s3://$S3_BUCKET/backups/$(basename "$COMPRESSED_FILE")"
    else
        print_warn "AWS CLI not installed, skipping S3 upload"
    fi
}

# Clean old backups
cleanup_old_backups() {
    print_info "Cleaning up backups older than $BACKUP_RETENTION_DAYS days..."

    # Local cleanup
    find "$BACKUP_DIR" -name "backup-*.sql.gz" -type f -mtime +$BACKUP_RETENTION_DAYS -delete
    REMAINING_BACKUPS=$(find "$BACKUP_DIR" -name "backup-*.sql.gz" -type f | wc -l)

    print_success "Cleanup completed. $REMAINING_BACKUPS backups remaining"

    # S3 cleanup (if enabled)
    if [ "$S3_ENABLED" = "true" ] && [ -n "$S3_BUCKET" ] && command -v aws > /dev/null 2>&1; then
        print_info "Cleaning up old S3 backups..."

        CUTOFF_DATE=$(date -d "$BACKUP_RETENTION_DAYS days ago" +%Y%m%d 2>/dev/null || date -v-${BACKUP_RETENTION_DAYS}d +%Y%m%d)

        aws s3 ls "s3://$S3_BUCKET/backups/" | while read -r line; do
            BACKUP_NAME=$(echo "$line" | awk '{print $4}')
            if [[ $BACKUP_NAME =~ backup-([0-9]{8}) ]]; then
                BACKUP_DATE="${BASH_REMATCH[1]}"
                if [ "$BACKUP_DATE" -lt "$CUTOFF_DATE" ]; then
                    print_info "Deleting old S3 backup: $BACKUP_NAME"
                    aws s3 rm "s3://$S3_BUCKET/backups/$BACKUP_NAME"
                fi
            fi
        done

        print_success "S3 cleanup completed"
    fi
}

# Verify backup integrity
verify_backup() {
    print_info "Verifying backup integrity..."

    if gzip -t "$COMPRESSED_FILE" 2>/dev/null; then
        print_success "Backup integrity verified"
    else
        print_error "Backup verification failed - file may be corrupted"
        exit 1
    fi
}

# Restore from backup (optional functionality)
restore_backup() {
    local backup_file=$1

    if [ -z "$backup_file" ]; then
        print_error "No backup file specified"
        echo "Usage: $0 restore <backup-file.sql.gz>"
        exit 1
    fi

    if [ ! -f "$backup_file" ]; then
        print_error "Backup file not found: $backup_file"
        exit 1
    fi

    print_warn "WARNING: This will restore the database from backup"
    read -p "Are you sure? (yes/no): " confirm

    if [ "$confirm" != "yes" ]; then
        print_info "Restore cancelled"
        exit 0
    fi

    print_info "Restoring from backup: $backup_file"

    # Decompress if needed
    if [[ $backup_file == *.gz ]]; then
        print_info "Decompressing backup..."
        gunzip -k "$backup_file"
        backup_file="${backup_file%.gz}"
    fi

    # Stop backend to prevent connection issues
    print_info "Stopping backend service..."
    docker-compose -f docker-compose.prod.yml stop backend

    # Drop and recreate database
    print_info "Recreating database..."
    docker exec "$DB_CONTAINER" psql -U postgres -c "DROP DATABASE IF EXISTS findtravelmate;"
    docker exec "$DB_CONTAINER" psql -U postgres -c "CREATE DATABASE findtravelmate;"

    # Restore backup
    print_info "Restoring data..."
    docker exec -i "$DB_CONTAINER" pg_restore -U postgres -d findtravelmate -v < "$backup_file"

    # Restart backend
    print_info "Starting backend service..."
    docker-compose -f docker-compose.prod.yml start backend

    print_success "Restore completed successfully"
}

# List available backups
list_backups() {
    print_info "Available backups:"
    echo ""

    if [ -d "$BACKUP_DIR" ]; then
        ls -lh "$BACKUP_DIR"/backup-*.sql.gz 2>/dev/null | awk '{print $9, "(" $5 ")"}'
    else
        print_warn "No backups found in $BACKUP_DIR"
    fi

    echo ""

    if [ "$S3_ENABLED" = "true" ] && [ -n "$S3_BUCKET" ] && command -v aws > /dev/null 2>&1; then
        print_info "S3 backups:"
        aws s3 ls "s3://$S3_BUCKET/backups/" --human-readable
    fi
}

# Show usage
show_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  backup          Create a new backup (default)"
    echo "  restore <file>  Restore from backup file"
    echo "  list            List available backups"
    echo "  help            Show this help message"
    echo ""
    echo "Configuration:"
    echo "  Set BACKUP_RETENTION_DAYS in .env (default: 7 days)"
    echo "  Set BACKUP_S3_ENABLED=true to enable S3 uploads"
    echo "  Set BACKUP_S3_BUCKET for S3 destination"
}

# Main function
main() {
    local command=${1:-backup}

    case "$command" in
        backup)
            print_info "Starting backup process..."
            print_info "Timestamp: $(date)"

            check_container
            create_backup_dir
            create_backup
            compress_backup
            verify_backup
            upload_to_s3
            cleanup_old_backups

            print_success "Backup completed successfully! 🎉"
            print_info "Backup location: $COMPRESSED_FILE"
            ;;

        restore)
            restore_backup "$2"
            ;;

        list)
            list_backups
            ;;

        help)
            show_usage
            ;;

        *)
            print_error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
