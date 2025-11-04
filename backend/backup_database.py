#!/usr/bin/env python3
"""
Database Backup Script for FindTravelMate

Creates a complete PostgreSQL database backup with all data.
Usage: python backup_database.py
"""

import os
import subprocess
import sys
from datetime import datetime
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


def create_backup():
    """Create a complete database backup."""
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        sys.exit(1)
    
    try:
        # Parse connection details
        db_config = parse_database_url(database_url)
        print(f"📊 Backing up database: {db_config['database']}")
        
        # Create backups directory
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file = backup_dir / f"backup_{timestamp}.sql"
        
        # Prepare pg_dump command
        env = os.environ.copy()
        if db_config['password']:
            env['PGPASSWORD'] = db_config['password']
        
        cmd = [
            'pg_dump',
            '--host', db_config['host'],
            '--port', db_config['port'],
            '--username', db_config['user'],
            '--dbname', db_config['database'],
            '--verbose',
            '--no-acl',
            '--no-owner',
            '--format=plain',
            '--file', str(backup_file)
        ]
        
        print(f"🔄 Creating backup: {backup_file}")
        
        # Execute backup
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Get file size
            file_size = backup_file.stat().st_size
            size_mb = file_size / (1024 * 1024)
            
            print(f"✅ Backup created successfully!")
            print(f"📁 File: {backup_file}")
            print(f"📊 Size: {size_mb:.1f} MB")
            
            # Count lines to estimate content
            with open(backup_file, 'r') as f:
                line_count = sum(1 for _ in f)
            print(f"📄 Lines: {line_count:,}")
            
        else:
            print(f"❌ Backup failed!")
            print(f"Error: {result.stderr}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 FindTravelMate Database Backup")
    print("=" * 40)
    create_backup()