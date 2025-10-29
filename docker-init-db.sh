#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
sleep 5

echo "Initializing database schema and data..."
docker-compose -f docker-compose.prod.yml exec -T backend python init_db.py

echo "Database initialized successfully!"
