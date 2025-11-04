#!/usr/bin/env python3
"""
Database Restoration Script for FindTravelMate

Restores a PostgreSQL database backup to the target database.
Based on the successful AWS deployment experience (November 2025).

Usage: 
    python restore_database.py backup_file.sql
    python restore_database.py --list                    # List available backups
    python restore_database.py --aws backup_file.sql     # For AWS deployment
"""

import os
import subprocess
import sys
from pathlib import Path
import re
import argparse


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


def test_connection(db_config):
    """Test database connection."""
    env = os.environ.copy()
    if db_config['password']:
        env['PGPASSWORD'] = db_config['password']
    
    cmd = [
        'psql',
        '--host', db_config['host'],
        '--port', db_config['port'],
        '--username', db_config['user'],
        '--dbname', 'postgres',  # Connect to default postgres database
        '--command', 'SELECT version();'
    ]
    
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    return result.returncode == 0


def database_exists(db_config):
    """Check if database exists."""
    env = os.environ.copy()
    if db_config['password']:
        env['PGPASSWORD'] = db_config['password']
    
    cmd = [
        'psql',
        '--host', db_config['host'],
        '--port', db_config['port'],
        '--username', db_config['user'],
        '--dbname', 'postgres',
        '--tuples-only',
        '--command', f"SELECT 1 FROM pg_database WHERE datname = '{db_config['database']}';"
    ]
    
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    return result.returncode == 0 and result.stdout.strip()


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
    
    # Check key data counts
    checks = [
        ("users", "👥 Users restored"),
        ("activities", "🎯 Activities restored"),
        ("categories", "📂 Categories restored"),
        ("destinations", "🌍 Destinations restored")
    ]
    
    for table, description in checks:
        cmd[7] = f"SELECT COUNT(*) FROM {table};"
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode == 0:
            count = result.stdout.strip()
            print(f"{description}: {count}")
    
    # Show category names for verification
    print("\n📂 Categories restored:")
    cmd[7] = "SELECT name FROM categories ORDER BY name;"
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if result.returncode == 0:
        categories = result.stdout.strip().split('\n')
        for cat in categories:
            if cat.strip():
                print(f"   • {cat.strip()}")


def restore_database_main(backup_file_path, aws_mode=False):
    """Main restoration function."""
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        if aws_mode:
            print("💡 For AWS, try: export DATABASE_URL='postgresql://ubuntu:ubuntu123@localhost:5432/findtravelmate'")
        else:
            print("💡 For local, try: export DATABASE_URL='postgresql://hongyusu@localhost:5432/findtravelmate'")
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
        print(f"🖥️  Mode: {'AWS' if aws_mode else 'Local'}")
        
        # Test connection
        print("\n🔍 Testing database connection...")
        if not test_connection(db_config):
            print("❌ Cannot connect to database server")
            if aws_mode:
                print("💡 Make sure PostgreSQL is running and ubuntu user exists")
            sys.exit(1)
        print("✅ Database connection successful")
        
        # Confirm destructive operation
        if database_exists(db_config):
            response = input(f"\n⚠️  Database '{db_config['database']}' exists and will be completely replaced. Continue? (y/N): ")
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
        print("\n🔍 Verifying restoration...")
        verify_restoration(db_config)
        
        print("\n✅ Database restoration completed successfully!")
        
        if aws_mode:
            print("\n🚀 Next steps for AWS deployment:")
            print("   1. Restart backend service: sudo systemctl restart findtravelmate-backend")
            print("   2. Check service status: sudo systemctl status findtravelmate-backend")
            print("   3. Test API: curl http://localhost:8000/api/v1/activities/categories")
        
    except Exception as e:
        print(f"❌ Error restoring database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Restore FindTravelMate database from backup')
    parser.add_argument('backup_file', nargs='?', help='Backup file to restore')
    parser.add_argument('--list', action='store_true', help='List available backup files')
    parser.add_argument('--aws', action='store_true', help='AWS deployment mode (provides AWS-specific guidance)')
    
    args = parser.parse_args()
    
    print("🚀 FindTravelMate Database Restoration")
    print("=" * 45)
    
    if args.list:
        list_backups()
    elif args.backup_file:
        restore_database_main(args.backup_file, aws_mode=args.aws)
    else:
        print("\nUsage:")
        print("  python restore_database.py backup_file.sql")
        print("  python restore_database.py backup_file.sql --aws")
        print("  python restore_database.py --list")
        print("\nExamples:")
        print("  python restore_database.py backups/backup_2025-11-04_22-45-58.sql")
        print("  python restore_database.py backup_2025-11-04_22-45-58.sql --aws")
        print("  python restore_database.py --list")
        
        # Show available backups
        print()
        list_backups()