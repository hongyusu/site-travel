"""Email service using Resend."""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
import resend
from jinja2 import Environment, FileSystemLoader, select_autoescape
import traceback

from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Resend client
resend.api_key = settings.RESEND_API_KEY

# Template directory
TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "emails"

# Initialize Jinja2 environment
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailService:
    """Email service for sending various types of emails."""
    
    @staticmethod
    def _render_template(template_name: str, context: Dict[str, Any]) -> tuple[str, str]:
        """Render both HTML and text versions of an email template."""
        try:
            # Render HTML template
            html_template = jinja_env.get_template(f"{template_name}.html")
            html_content = html_template.render(**context)
            
            # Try to render text template, fallback to HTML if not available
            try:
                text_template = jinja_env.get_template(f"{template_name}.txt")
                text_content = text_template.render(**context)
            except:
                # Simple HTML to text conversion
                import re
                text_content = re.sub('<[^<]+?>', '', html_content)
                text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            return html_content, text_content
        except Exception as e:
            logger.error(f"Error rendering template {template_name}: {e}")
            logger.error(f"Template rendering traceback: {traceback.format_exc()}")
            raise
    
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        template_name: str,
        context: Dict[str, Any],
        to_name: Optional[str] = None
    ) -> bool:
        """Send an email using Resend."""
        if not settings.EMAIL_ENABLED:
            logger.info(f"Email disabled, skipping email to {to_email}")
            return True
        
        # Handle testing mode - redirect all emails to verified address
        original_email = to_email
        original_name = to_name
        
        if settings.EMAIL_TESTING_MODE:
            to_email = settings.EMAIL_TEST_RECIPIENT
            to_name = "Test Recipient"
            logger.info(f"Testing mode: redirecting email from {original_email} to {to_email}")
            
            # Add original recipient info to email context for transparency
            context = context.copy()
            context["original_recipient"] = original_email
            context["original_recipient_name"] = original_name
            subject = f"[TEST] {subject} (intended for: {original_email})"
        
        try:
            # Render templates
            html_content, text_content = EmailService._render_template(template_name, context)
            
            # Prepare email data
            email_data = {
                "from": f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>",
                "to": [to_email],  # Simplified - just use the email address
                "subject": subject,
                "html": html_content,
                "text": text_content,
            }
            
            # Send email
            response = resend.Emails.send(email_data)
            logger.info(f"Email sent successfully to {to_email} (original: {original_email}): {response}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email} (original: {original_email}): {e}")
            logger.error(f"Email sending traceback: {traceback.format_exc()}")
            return False
    
    @staticmethod
    def send_welcome_email(user_email: str, user_name: str) -> bool:
        """Send welcome email to new user."""
        context = {
            "user_name": user_name,
            "app_name": settings.APP_NAME,
        }
        
        return EmailService.send_email(
            to_email=user_email,
            to_name=user_name,
            subject=f"Welcome to {settings.APP_NAME}!",
            template_name="welcome",
            context=context
        )
    
    @staticmethod
    def send_vendor_welcome_email(user_email: str, user_name: str, company_name: str) -> bool:
        """Send welcome email to new vendor."""
        context = {
            "user_name": user_name,
            "company_name": company_name,
            "app_name": settings.APP_NAME,
        }
        
        return EmailService.send_email(
            to_email=user_email,
            to_name=user_name,
            subject=f"Welcome to {settings.APP_NAME} - Vendor Account Created",
            template_name="vendor_welcome",
            context=context
        )
    
    @staticmethod
    def send_booking_confirmation_email(
        user_email: str,
        user_name: str,
        booking_reference: str,
        activity_title: str,
        booking_date: str,
        total_amount: str
    ) -> bool:
        """Send booking confirmation email."""
        context = {
            "user_name": user_name,
            "booking_reference": booking_reference,
            "activity_title": activity_title,
            "booking_date": booking_date,
            "total_amount": total_amount,
            "app_name": settings.APP_NAME,
        }
        
        return EmailService.send_email(
            to_email=user_email,
            to_name=user_name,
            subject=f"Booking Confirmation - {booking_reference}",
            template_name="booking_confirmation",
            context=context
        )
    
    @staticmethod
    def send_booking_status_email(
        user_email: str,
        user_name: str,
        booking_reference: str,
        activity_title: str,
        status: str,
        message: Optional[str] = None
    ) -> bool:
        """Send booking status change email."""
        status_messages = {
            "approved": "Your booking has been approved!",
            "rejected": "Your booking has been rejected.",
            "cancelled": "Your booking has been cancelled.",
            "completed": "Your booking has been completed.",
        }
        
        context = {
            "user_name": user_name,
            "booking_reference": booking_reference,
            "activity_title": activity_title,
            "status": status,
            "status_message": status_messages.get(status, f"Your booking status has been updated to {status}."),
            "message": message,
            "app_name": settings.APP_NAME,
        }
        
        return EmailService.send_email(
            to_email=user_email,
            to_name=user_name,
            subject=f"Booking Update - {booking_reference}",
            template_name="booking_status",
            context=context
        )
    
    @staticmethod
    def send_review_request_email(
        user_email: str,
        user_name: str,
        activity_title: str,
        booking_reference: str
    ) -> bool:
        """Send review request email after completed booking."""
        context = {
            "user_name": user_name,
            "activity_title": activity_title,
            "booking_reference": booking_reference,
            "app_name": settings.APP_NAME,
        }
        
        return EmailService.send_email(
            to_email=user_email,
            to_name=user_name,
            subject=f"How was your experience? - {activity_title}",
            template_name="review_request",
            context=context
        )