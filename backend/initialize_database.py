#!/usr/bin/env python3
"""
Database Initialization Script for FinuoTravel

Initializes a brand new database from a backup file.
Based on successful AWS deployment experience (November 2025).

Usage: 
    python initialize_database.py backup_file.sql
    python initialize_database.py --list
    python initialize_database.py --aws backup_file.sql  # For AWS deployment
"""

import os
import subprocess
import sys
from pathlib import Path
import re


def parse_database_url(database_url):
    """Parse DATABASE_URL to extract connection components."""
    pattern = r'postgresql://([^:]+):?([^@]*)@([^:]+):(\d+)/(.+)'
    match = re.match(pattern, database_url)
    
    if not match:
        raise ValueError(f"Invalid DATABASE_URL format: {database_url}")
    
    return {
        'user': match.group(1),
        'password': match.group(2),
        'host': match.group(3),
        'port': match.group(4),
        'database': match.group(5)
    }


def list_backups():
    """List available backup files."""
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("📁 No backups directory found")
        return []
    
    backup_files = list(backup_dir.glob("backup_*.sql"))
    if not backup_files:
        print("📁 No backup files found in backups/")
        return []
    
    print("📁 Available backups:")
    for backup_file in sorted(backup_files, reverse=True):
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        print(f"   {backup_file.name} ({size_mb:.1f} MB)")
    
    return backup_files


def drop_database(db_config):
    """Drop the existing database."""
    env = os.environ.copy()
    if db_config['password']:
        env['PGPASSWORD'] = db_config['password']
    
    cmd = [
        'dropdb',
        '--host', db_config['host'],
        '--port', db_config['port'],
        '--username', db_config['user'],
        '--if-exists',
        db_config['database']
    ]
    
    print(f"🗑️  Dropping database: {db_config['database']}")
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"⚠️  Warning: {result.stderr.strip()}")


def create_database(db_config):
    """Create a fresh database."""
    env = os.environ.copy()
    if db_config['password']:
        env['PGPASSWORD'] = db_config['password']
    
    cmd = [
        'createdb',
        '--host', db_config['host'],
        '--port', db_config['port'],
        '--username', db_config['user'],
        db_config['database']
    ]
    
    print(f"🆕 Creating database: {db_config['database']}")
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to create database: {result.stderr}")
        sys.exit(1)


def restore_database(db_config, backup_file):
    """Restore database from backup file."""
    env = os.environ.copy()
    if db_config['password']:
        env['PGPASSWORD'] = db_config['password']
    
    cmd = [
        'psql',
        '--host', db_config['host'],
        '--port', db_config['port'],
        '--username', db_config['user'],
        '--dbname', db_config['database'],
        '--file', str(backup_file),
        '--quiet'
    ]
    
    print(f"📥 Restoring from: {backup_file}")
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Restoration failed: {result.stderr}")
        sys.exit(1)


def verify_restoration(db_config):
    """Verify the restored database."""
    env = os.environ.copy()
    if db_config['password']:
        env['PGPASSWORD'] = db_config['password']
    
    # Check table count
    cmd = [
        'psql',
        '--host', db_config['host'],
        '--port', db_config['port'],
        '--username', db_config['user'],
        '--dbname', db_config['database'],
        '--tuples-only',
        '--command', "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
    ]
    
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if result.returncode == 0:
        table_count = result.stdout.strip()
        print(f"📊 Tables restored: {table_count}")
    
    # Check user count
    cmd[7] = "SELECT COUNT(*) FROM users;"
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if result.returncode == 0:
        user_count = result.stdout.strip()
        print(f"👥 Users restored: {user_count}")
    
    # Check activity count
    cmd[7] = "SELECT COUNT(*) FROM activities;"
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if result.returncode == 0:
        activity_count = result.stdout.strip()
        print(f"🎯 Activities restored: {activity_count}")


def initialize_database(backup_file_path):
    """Initialize database from backup."""
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        sys.exit(1)
    
    try:
        # Parse connection details
        db_config = parse_database_url(database_url)
        
        # Verify backup file exists
        backup_file = Path(backup_file_path)
        if not backup_file.exists():
            print(f"❌ Backup file not found: {backup_file}")
            sys.exit(1)
        
        print(f"🎯 Target database: {db_config['database']}")
        print(f"📁 Backup file: {backup_file}")
        
        # Confirm destructive operation
        response = input("\n⚠️  This will completely replace the current database. Continue? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled")
            sys.exit(0)
        
        # Drop existing database
        drop_database(db_config)
        
        # Create fresh database
        create_database(db_config)
        
        # Restore from backup
        restore_database(db_config, backup_file)
        
        # Verify restoration
        verify_restoration(db_config)
        
        print("\n✅ Database initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 FinuoTravel Database Initialization")
    print("=" * 45)
    
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        list_backups()
    elif len(sys.argv) == 2:
        backup_file = sys.argv[1]
        initialize_database(backup_file)
    else:
        print("\nUsage:")
        print("  python initialize_database.py backup_file.sql")
        print("  python initialize_database.py --list")
        print("\nExamples:")
        print("  python initialize_database.py backups/backup_2024-01-15_14-30-25.sql")
        print("  python initialize_database.py --list")
        
        # Show available backups
        print()
        list_backups()