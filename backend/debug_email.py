#!/usr/bin/env python3
"""Debug email service to see what data is being sent."""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from app.services.email import EmailService
from app.config import settings
import resend

def debug_email_service():
    """Debug the email service to see what's happening."""
    print("=== EMAIL SERVICE DEBUG ===")
    print(f"EMAIL_ENABLED: {settings.EMAIL_ENABLED}")
    print(f"EMAIL_TESTING_MODE: {settings.EMAIL_TESTING_MODE}")
    print(f"EMAIL_TEST_RECIPIENT: {settings.EMAIL_TEST_RECIPIENT}")
    print(f"EMAIL_FROM: {settings.EMAIL_FROM}")
    print(f"EMAIL_FROM_NAME: {settings.EMAIL_FROM_NAME}")
    print(f"RESEND_API_KEY: {settings.RESEND_API_KEY[:10]}...")
    
    # Test with our service
    print("\n=== TESTING EMAIL SERVICE ===")
    
    # Temporarily disable testing mode to see the exact error
    original_mode = settings.EMAIL_TESTING_MODE
    settings.EMAIL_TESTING_MODE = False
    
    try:
        # Create the context manually to see what we're sending
        context = {
            "user_name": "Hongyu Su",
            "app_name": settings.APP_NAME,
        }
        
        print(f"Context: {context}")
        
        # Render template to see what's generated
        html_content, text_content = EmailService._render_template("welcome", context)
        print(f"HTML length: {len(html_content)}")
        print(f"Text length: {len(text_content)}")
        
        # Prepare email data like the service does
        email_data = {
            "from": f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>",
            "to": ["hongyu.su.uh@gmail.com"],
            "subject": f"Welcome to {settings.APP_NAME}!",
            "html": html_content,
            "text": text_content,
        }
        
        print(f"Email data: {email_data}")
        
        # Try to send with raw resend
        response = resend.Emails.send(email_data)
        print(f"✅ Raw send successful: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        settings.EMAIL_TESTING_MODE = original_mode

if __name__ == "__main__":
    debug_email_service()