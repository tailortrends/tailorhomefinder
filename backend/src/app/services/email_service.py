"""
Email service for sending notifications
"""
from fastapi_mail import FastMail, MessageSchema, MessageType
from typing import Optional, List
from datetime import datetime
import logging

from ..core.email_config import get_email_config, email_settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending email notifications"""

    def __init__(self):
        self.config = get_email_config()
        self.fast_mail = FastMail(self.config)
        self.enabled = email_settings.EMAIL_ENABLED

    async def send_email(
        self,
        to_emails: List[str],
        subject: str,
        template_name: str,
        template_data: dict,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email using a template

        Args:
            to_emails: List of recipient email addresses
            subject: Email subject line
            template_name: Name of the template file (without .html)
            template_data: Dictionary of data to pass to the template
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not self.enabled:
            logger.info(f"Email sending disabled. Would send to: {to_emails}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Template: {template_name}")
            logger.debug(f"Data: {template_data}")
            return True  # Return True for development purposes

        try:
            message = MessageSchema(
                subject=subject,
                recipients=to_emails,
                template_body=template_data,
                subtype=MessageType.html,
                cc=cc or [],
                bcc=bcc or []
            )

            await self.fast_mail.send_message(message, template_name=f"{template_name}.html")
            logger.info(f"Email sent successfully to {to_emails}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_emails}: {str(e)}")
            return False

    async def send_inquiry_notification(
        self,
        inquiry_id: str,
        name: str,
        email: str,
        phone: str,
        message: str,
        inquiry_type: str,
        property_address: Optional[str] = None,
        property_price: Optional[int] = None,
        agent_email: Optional[str] = None
    ) -> bool:
        """
        Send notification email to admin/agent about new inquiry

        Args:
            inquiry_id: Unique identifier for the inquiry
            name: Name of the person making the inquiry
            email: Email of the person making the inquiry
            phone: Phone number of the person making the inquiry
            message: The inquiry message
            inquiry_type: Type of inquiry (general, schedule_tour, etc.)
            property_address: Address of the property (optional)
            property_price: Price of the property (optional)
            agent_email: Email of the listing agent (optional)

        Returns:
            bool: True if sent successfully
        """
        # Determine recipient - agent email if available, otherwise admin
        recipient = agent_email if agent_email else email_settings.ADMIN_EMAIL

        template_data = {
            "inquiry_id": inquiry_id,
            "name": name,
            "email": email,
            "phone": phone,
            "message": message,
            "inquiry_type": inquiry_type,
            "property_address": property_address,
            "property_price": property_price,
            "created_at": datetime.now().strftime("%B %d, %Y at %I:%M %p")
        }

        subject = f"New Property Inquiry from {name}"
        if inquiry_type == "schedule_tour":
            subject = f"Tour Request from {name}"
        elif inquiry_type == "make_offer":
            subject = f"Offer Inquiry from {name}"

        return await self.send_email(
            to_emails=[recipient],
            subject=subject,
            template_name="inquiry_notification",
            template_data=template_data,
            bcc=[email_settings.ADMIN_EMAIL] if agent_email else None
        )

    async def send_inquiry_confirmation(
        self,
        inquiry_id: str,
        name: str,
        email: str,
        inquiry_type: str,
        property_address: Optional[str] = None,
        property_price: Optional[int] = None
    ) -> bool:
        """
        Send confirmation email to the person who made the inquiry

        Args:
            inquiry_id: Unique identifier for the inquiry
            name: Name of the person making the inquiry
            email: Email to send confirmation to
            inquiry_type: Type of inquiry
            property_address: Address of the property (optional)
            property_price: Price of the property (optional)

        Returns:
            bool: True if sent successfully
        """
        template_data = {
            "inquiry_id": inquiry_id,
            "name": name,
            "property_address": property_address,
            "property_price": property_price
        }

        # Use appropriate template based on inquiry type
        if inquiry_type == "schedule_tour":
            template_name = "tour_scheduled"
            subject = "Your Tour Request - TailorHomeFinder"
        else:
            template_name = "inquiry_confirmation"
            subject = "Thank You for Your Inquiry - TailorHomeFinder"

        return await self.send_email(
            to_emails=[email],
            subject=subject,
            template_name=template_name,
            template_data=template_data
        )


# Singleton instance
email_service = EmailService()


async def send_inquiry_emails(
    inquiry_id: str,
    name: str,
    email: str,
    phone: str,
    message: str,
    inquiry_type: str,
    property_address: Optional[str] = None,
    property_price: Optional[int] = None,
    agent_email: Optional[str] = None
) -> dict:
    """
    Send both notification and confirmation emails for an inquiry

    Returns:
        dict: Status of both email sends
    """
    # Send notification to admin/agent
    notification_sent = await email_service.send_inquiry_notification(
        inquiry_id=inquiry_id,
        name=name,
        email=email,
        phone=phone,
        message=message,
        inquiry_type=inquiry_type,
        property_address=property_address,
        property_price=property_price,
        agent_email=agent_email
    )

    # Send confirmation to the inquirer
    confirmation_sent = await email_service.send_inquiry_confirmation(
        inquiry_id=inquiry_id,
        name=name,
        email=email,
        inquiry_type=inquiry_type,
        property_address=property_address,
        property_price=property_price
    )

    return {
        "notification_sent": notification_sent,
        "confirmation_sent": confirmation_sent
    }
