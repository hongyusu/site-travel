#!/usr/bin/env python3
"""Test script for email functionality."""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from app.services.email import EmailService

def test_welcome_email():
    """Test sending a welcome email."""
    print("Testing welcome email...")
    result = EmailService.send_welcome_email(
        user_email="test@example.com",
        user_name="Test User"
    )
    print(f"Welcome email result: {result}")
    return result

def test_booking_confirmation_email():
    """Test sending a booking confirmation email."""
    print("Testing booking confirmation email...")
    result = EmailService.send_booking_confirmation_email(
        user_email="test@example.com",
        user_name="Test User",
        booking_reference="TEST123",
        activity_title="Test Activity",
        booking_date="November 10, 2024 at 2:00 PM",
        total_amount="€50.00"
    )
    print(f"Booking confirmation email result: {result}")
    return result

def test_vendor_welcome_email():
    """Test sending a vendor welcome email."""
    print("Testing vendor welcome email...")
    result = EmailService.send_vendor_welcome_email(
        user_email="vendor@example.com",
        user_name="Test Vendor",
        company_name="Test Company Ltd"
    )
    print(f"Vendor welcome email result: {result}")
    return result

def test_booking_status_email():
    """Test sending a booking status email."""
    print("Testing booking status email...")
    result = EmailService.send_booking_status_email(
        user_email="test@example.com",
        user_name="Test User",
        booking_reference="TEST123",
        activity_title="Test Activity",
        status="approved"
    )
    print(f"Booking status email result: {result}")
    return result

def test_review_request_email():
    """Test sending a review request email."""
    print("Testing review request email...")
    result = EmailService.send_review_request_email(
        user_email="test@example.com",
        user_name="Test User",
        activity_title="Test Activity",
        booking_reference="TEST123"
    )
    print(f"Review request email result: {result}")
    return result

if __name__ == "__main__":
    print("Starting email functionality tests...\n")
    
    # Run all tests
    tests = [
        test_welcome_email,
        test_booking_confirmation_email,
        test_vendor_welcome_email,
        test_booking_status_email,
        test_review_request_email
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print("✅ Test passed\n")
        except Exception as e:
            print(f"❌ Test failed: {e}\n")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    print(f"Email functionality test summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All email tests passed!")
    else:
        print("⚠️  Some email tests failed. Check the logs above.")