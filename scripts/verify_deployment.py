#!/usr/bin/env python3
"""
Deployment Verification Script for FindTravelMate

Verifies that both local and AWS deployments are working correctly.
Based on the successful deployment experience (November 2025).

Usage:
    python verify_deployment.py --local          # Verify local deployment
    python verify_deployment.py --aws            # Verify AWS deployment  
    python verify_deployment.py --compare        # Compare local vs AWS data
"""

import os
import sys
import subprocess
import requests
import time
import argparse
from pathlib import Path


class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_header(title):
    print(f"{Colors.BLUE}🚀 {title}{Colors.NC}")
    print("=" * (len(title) + 4))


def print_step(message):
    print(f"{Colors.BLUE}📍 {message}{Colors.NC}")


def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")


def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")


def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")


def test_database_connection(db_url, description):
    """Test database connectivity and return basic stats."""
    print_step(f"Testing {description} database...")
    
    try:
        # Test connection
        result = subprocess.run(
            ['psql', db_url, '-c', 'SELECT version();'],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode != 0:
            print_error(f"Cannot connect to {description} database")
            return None
        
        # Get database stats
        queries = [
            ("tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"),
            ("users", "SELECT COUNT(*) FROM users;"),
            ("activities", "SELECT COUNT(*) FROM activities;"),
            ("categories", "SELECT COUNT(*) FROM categories;"),
            ("destinations", "SELECT COUNT(*) FROM destinations;")
        ]
        
        stats = {}
        for name, query in queries:
            result = subprocess.run(
                ['psql', db_url, '--tuples-only', '-c', query],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                stats[name] = int(result.stdout.strip())
        
        print_success(f"{description} database connection successful")
        for name, count in stats.items():
            print(f"   {name.capitalize()}: {count}")
        
        return stats
        
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        return None


def test_api_endpoints(base_url, description):
    """Test API endpoints and return response data."""
    print_step(f"Testing {description} API endpoints...")
    
    endpoints = [
        ("/api/v1/activities/categories", "Categories"),
        ("/api/v1/activities/destinations", "Destinations"),
        ("/api/v1/activities/search?limit=5", "Activities")
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    count = len(data)
                elif isinstance(data, dict) and 'data' in data:
                    count = len(data['data'])
                else:
                    count = 1
                
                results[name.lower()] = count
                print_success(f"{name} endpoint: {count} items")
            else:
                print_error(f"{name} endpoint failed: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print_error(f"{name} endpoint failed: {e}")
            return None
    
    return results


def test_frontend(base_url, description):
    """Test frontend accessibility."""
    print_step(f"Testing {description} frontend...")
    
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200 and 'FindTravelMate' in response.text:
            print_success(f"{description} frontend is accessible")
            return True
        else:
            print_error(f"{description} frontend test failed")
            return False
            
    except Exception as e:
        print_error(f"{description} frontend test failed: {e}")
        return False


def verify_local_deployment():
    """Verify local deployment."""
    print_header("Local Deployment Verification")
    
    # Test database
    local_db_url = os.getenv('DATABASE_URL', 'postgresql://hongyusu@localhost:5432/findtravelmate')
    db_stats = test_database_connection(local_db_url, "local")
    
    if not db_stats:
        return False
    
    # Test API
    api_results = test_api_endpoints("http://localhost:8000", "local")
    if not api_results:
        return False
    
    # Test frontend
    frontend_ok = test_frontend("http://localhost:3000", "local")
    
    # Summary
    print("\n📊 Local Deployment Summary:")
    print(f"   Database: {db_stats.get('activities', 0)} activities, {db_stats.get('categories', 0)} categories")
    print(f"   API: {api_results.get('activities', 0)} activities, {api_results.get('categories', 0)} categories")
    print(f"   Frontend: {'✅ Working' if frontend_ok else '❌ Failed'}")
    
    return db_stats and api_results and frontend_ok


def verify_aws_deployment():
    """Verify AWS deployment."""
    print_header("AWS Deployment Verification")
    
    aws_host = "ec2-54-217-173-125.eu-west-1.compute.amazonaws.com"
    
    # Test API
    api_results = test_api_endpoints(f"http://{aws_host}:8000", "AWS")
    if not api_results:
        return False
    
    # Test frontend
    frontend_ok = test_frontend(f"http://{aws_host}:3000", "AWS")
    
    # Test SSH connectivity (optional)
    pem_file = Path("ocrbot.pem")
    if pem_file.exists():
        print_step("Testing SSH connectivity...")
        try:
            result = subprocess.run(
                ['ssh', '-i', str(pem_file), '-o', 'ConnectTimeout=10', 
                 f'ubuntu@{aws_host}', 'echo "SSH test successful"'],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                print_success("SSH connectivity working")
                
                # Get database stats via SSH
                print_step("Getting AWS database stats via SSH...")
                db_cmd = '''
                export PGPASSWORD=ubuntu123
                echo "Activities: $(psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate --tuples-only -c 'SELECT COUNT(*) FROM activities;' | xargs)"
                echo "Categories: $(psql --host localhost --port 5432 --username ubuntu --dbname findtravelmate --tuples-only -c 'SELECT COUNT(*) FROM categories;' | xargs)"
                '''
                result = subprocess.run(
                    ['ssh', '-i', str(pem_file), f'ubuntu@{aws_host}', db_cmd],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    print("   " + result.stdout.strip().replace('\n', '\n   '))
                
            else:
                print_warning("SSH connectivity failed (but API/frontend working)")
        except Exception as e:
            print_warning(f"SSH test failed: {e}")
    
    # Summary
    print("\n📊 AWS Deployment Summary:")
    print(f"   API: {api_results.get('activities', 0)} activities, {api_results.get('categories', 0)} categories")
    print(f"   Frontend: {'✅ Working' if frontend_ok else '❌ Failed'}")
    print(f"   URLs: http://{aws_host}:3000 (frontend), http://{aws_host}:8000/api/v1 (API)")
    
    return api_results and frontend_ok


def compare_deployments():
    """Compare local and AWS deployments."""
    print_header("Local vs AWS Comparison")
    
    # Get local data
    print_step("Getting local deployment data...")
    local_api = test_api_endpoints("http://localhost:8000", "local")
    
    # Get AWS data
    print_step("Getting AWS deployment data...")
    aws_host = "ec2-54-217-173-125.eu-west-1.compute.amazonaws.com"
    aws_api = test_api_endpoints(f"http://{aws_host}:8000", "AWS")
    
    if not local_api or not aws_api:
        print_error("Cannot compare - one or both deployments are not accessible")
        return False
    
    # Compare data
    print("\n📊 Deployment Comparison:")
    print(f"{'Metric':<15} {'Local':<10} {'AWS':<10} {'Match'}")
    print("-" * 45)
    
    all_match = True
    for metric in ['categories', 'destinations', 'activities']:
        local_count = local_api.get(metric, 0)
        aws_count = aws_api.get(metric, 0)
        match = "✅" if local_count == aws_count else "❌"
        if local_count != aws_count:
            all_match = False
        
        print(f"{metric.capitalize():<15} {local_count:<10} {aws_count:<10} {match}")
    
    print()
    if all_match:
        print_success("✅ All data counts match between local and AWS")
    else:
        print_warning("⚠️  Data counts don't match - consider running database sync")
    
    return all_match


def main():
    parser = argparse.ArgumentParser(description='Verify FindTravelMate deployment')
    parser.add_argument('--local', action='store_true', help='Verify local deployment')
    parser.add_argument('--aws', action='store_true', help='Verify AWS deployment')
    parser.add_argument('--compare', action='store_true', help='Compare local vs AWS')
    parser.add_argument('--all', action='store_true', help='Run all verifications')
    
    args = parser.parse_args()
    
    if not any([args.local, args.aws, args.compare, args.all]):
        parser.print_help()
        return
    
    success = True
    
    if args.local or args.all:
        success &= verify_local_deployment()
        print()
    
    if args.aws or args.all:
        success &= verify_aws_deployment()
        print()
    
    if args.compare or args.all:
        success &= compare_deployments()
        print()
    
    if success:
        print_success("🎉 All verifications passed!")
    else:
        print_error("❌ Some verifications failed")
        sys.exit(1)


if __name__ == "__main__":
    main()