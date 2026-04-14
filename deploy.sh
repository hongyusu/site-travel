#!/bin/bash
set -e

# FindTravelMate - Single command deploy
# Usage:
#   ./deploy.sh                    # Deploy on localhost
#   ./deploy.sh 123.45.67.89       # Deploy with server IP (sets NEXT_PUBLIC_API_URL)

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

SERVER_IP="${1:-localhost}"
API_URL="http://${SERVER_IP}/api"

echo "=== FindTravelMate Deploy ==="
echo "Server: ${SERVER_IP}"
echo "API URL: ${API_URL}"
echo ""

# Export so docker-compose.yml can read it via ${NEXT_PUBLIC_API_URL:-default}
export NEXT_PUBLIC_API_URL="${API_URL}"

# Build and start
echo "Building and starting services..."
docker compose up -d --build

# Wait for health (always check localhost since we're running on the machine)
echo "Waiting for services to be healthy..."
for i in $(seq 1 30); do
    if curl -sf http://localhost/health > /dev/null 2>&1; then
        echo -e "${GREEN}All services are up!${NC}"
        echo ""
        echo "  Frontend:  http://${SERVER_IP}"
        echo "  API Docs:  http://${SERVER_IP}/docs"
        echo "  Admin:     http://${SERVER_IP}/admin/dashboard"
        echo ""
        echo "  Demo accounts:"
        echo "    Admin:    admin@findtravelmate.com / admin123"
        echo "    Customer: customer@example.com / customer123"
        echo "    Vendor:   vendor1@example.com / vendor123"
        echo ""

        # Check if DB has data
        ACTIVITY_COUNT=$(docker exec findtravelmate_db psql -U postgres -d findtravelmate -tAc "SELECT count(*) FROM activities;" 2>/dev/null || echo "0")
        if [ "$ACTIVITY_COUNT" -eq "0" ] 2>/dev/null; then
            echo -e "${RED}Database is empty!${NC} Restore demo data with:"
            echo "  docker exec -i findtravelmate_db psql -U postgres -d findtravelmate < backend/backups/backup_2026-04-14_expanded.sql"
        else
            echo "  Database: ${ACTIVITY_COUNT} activities loaded"
        fi
        exit 0
    fi
    echo "  Waiting... (${i}/30)"
    sleep 3
done

echo -e "${RED}Services did not become healthy in time.${NC}"
echo "Check logs: docker compose logs"
exit 1
