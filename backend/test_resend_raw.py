#!/usr/bin/env python3
"""Raw test of Resend API without our service layer."""

import resend

# Set API key
resend.api_key = "re_W314AQWC_AWo6mye59GD11pSfZ8533yG4"

def test_raw_resend():
    """Test Resend API directly."""
    try:
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": ["hongyu.su.uh@gmail.com"],
            "subject": "Test Email",
            "html": "<h1>Test</h1><p>This is a test email.</p>",
            "text": "Test - This is a test email."
        })
        print(f"✅ Email sent successfully: {response}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing raw Resend API...")
    test_raw_resend()