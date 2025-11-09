#!/usr/bin/env python3
"""Simple test to verify Resend API key works."""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from app.services.email import EmailService

def test_direct_email():
    """Test sending email directly to verified address."""
    print("Testing direct email to verified address...")
    
    # Override testing mode temporarily
    from app.config import settings
    original_testing_mode = settings.EMAIL_TESTING_MODE
    settings.EMAIL_TESTING_MODE = False
    
    try:
        result = EmailService.send_welcome_email(
            user_email="hongyu.su.uh@gmail.com",
            user_name="Hongyu Su"
        )
        print(f"Direct email result: {result}")
        return result
    finally:
        # Restore testing mode
        settings.EMAIL_TESTING_MODE = original_testing_mode

if __name__ == "__main__":
    print("Testing direct email to verified address...")
    result = test_direct_email()
    
    if result:
        print("✅ Direct email test passed!")
    else:
        print("❌ Direct email test failed!")