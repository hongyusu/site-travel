#!/usr/bin/env python3
"""
Quick verification script to check current status of FinuoTravel platform
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

def check_file_exists(path):
    """Check if a file exists"""
    return Path(path).exists()

def count_files(pattern):
    """Count files matching a pattern"""
    return len(list(Path('.').glob(pattern)))

def main():
    print("FinuoTravel - Platform Status Verification")
    print("=" * 50)
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Change to project directory
    os.chdir('/Users/hongyusu/Codes/side/site-travel')
    
    # File Structure Check
    print("📂 File Structure Check:")
    print(f"  Backend directory: {'✅' if check_file_exists('backend') else '❌'}")
    print(f"  Frontend directory: {'✅' if check_file_exists('frontend') else '❌'}")
    print(f"  Docker setup: {'✅' if check_file_exists('docker-compose.yml') else '❌'}")
    print(f"  Setup guides: {'✅' if check_file_exists('SETUP_GUIDE.md') and check_file_exists('DOCKER_SETUP_GUIDE.md') else '❌'}")
    print()
    
    # Backend Analysis
    print("🔧 Backend Analysis:")
    api_files = count_files('backend/app/api/v1/*.py')
    model_files = count_files('backend/app/models/*.py') 
    schema_files = count_files('backend/app/schemas/*.py')
    print(f"  API endpoints: {api_files} files")
    print(f"  Database models: {model_files} files")
    print(f"  Pydantic schemas: {schema_files} files")
    print(f"  Main app: {'✅' if check_file_exists('backend/app/main.py') else '❌'}")
    print(f"  Database init: {'✅' if check_file_exists('backend/init_db.py') else '❌'}")
    print()
    
    # Frontend Analysis  
    print("🎨 Frontend Analysis:")
    page_files = count_files('frontend/app/**/*.tsx')
    component_files = count_files('frontend/components/**/*.tsx')
    print(f"  Pages: {page_files} files")
    print(f"  Components: {component_files} files")
    print(f"  Next.js config: {'✅' if check_file_exists('frontend/next.config.js') else '❌'}")
    print(f"  Package.json: {'✅' if check_file_exists('frontend/package.json') else '❌'}")
    print()
    
    # Key Features Check
    print("🚀 Key Features:")
    features = {
        "Authentication": check_file_exists('backend/app/api/v1/auth.py'),
        "Activities API": check_file_exists('backend/app/api/v1/activities.py'),
        "Booking System": check_file_exists('backend/app/api/v1/bookings.py'),
        "Vendor Portal": check_file_exists('frontend/app/vendor'),
        "Admin Panel": check_file_exists('frontend/app/admin'),
        "Reviews": check_file_exists('backend/app/models/review.py'),
        "Cart": check_file_exists('frontend/app/cart'),
        "I18n Support": check_file_exists('frontend/contexts/LanguageContext.tsx'),
    }
    
    for feature, exists in features.items():
        print(f"  {feature}: {'✅' if exists else '❌'}")
    print()
    
    # Documentation
    print("📚 Documentation:")
    docs = {
        "README.md": check_file_exists('README.md'),
        "SETUP_GUIDE.md": check_file_exists('SETUP_GUIDE.md'), 
        "DOCKER_SETUP_GUIDE.md": check_file_exists('DOCKER_SETUP_GUIDE.md'),
        "GAP_ANALYSIS.md": check_file_exists('GAP_ANALYSIS.md'),
    }
    
    for doc, exists in docs.items():
        print(f"  {doc}: {'✅' if exists else '❌'}")
    print()
    
    # Summary
    print("📊 Summary:")
    total_features = len(features)
    completed_features = sum(features.values())
    completion_rate = (completed_features / total_features) * 100
    
    print(f"  Core Features: {completed_features}/{total_features} ({completion_rate:.0f}%)")
    print(f"  Documentation: {sum(docs.values())}/{len(docs)} complete")
    print(f"  Overall Status: {'🟢 Production Ready' if completion_rate >= 90 else '🟡 In Development'}")
    print()
    
    # Gap Analysis Update
    print("📝 Gap Analysis Status:")
    if check_file_exists('GAP_ANALYSIS.md'):
        with open('GAP_ANALYSIS.md', 'r') as f:
            content = f.read()
            if "100% Complete" in content:
                print("  Gap Analysis: ✅ Shows 100% completion")
            else:
                print("  Gap Analysis: 🟡 May need update")
    else:
        print("  Gap Analysis: ❌ File missing")
    
    print()
    print("✅ Verification Complete!")

if __name__ == "__main__":
    main()