"""
Email configuration for TailorHomeFinder notifications
"""
from pydantic_settings import BaseSettings
from fastapi_mail import ConnectionConfig
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class EmailSettings(BaseSettings):
    """Email configuration settings"""

    # SMTP Configuration
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "noreply@tailorhomefinder.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "TailorHomeFinder")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "True").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "False").lower() == "true"
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS", "True").lower() == "true"
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS", "True").lower() == "true"

    # Application Settings
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@tailorhomefinder.com")
    SUPPORT_EMAIL: str = os.getenv("SUPPORT_EMAIL", "support@tailorhomefinder.com")

    # Feature Flags
    EMAIL_ENABLED: bool = os.getenv("EMAIL_ENABLED", "False").lower() == "true"

    class Config:
        env_file = ".env"
        extra = "allow"


email_settings = EmailSettings()


def get_email_config() -> ConnectionConfig:
    """Get FastAPI-Mail connection configuration"""
    return ConnectionConfig(
        MAIL_USERNAME=email_settings.MAIL_USERNAME,
        MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
        MAIL_FROM=email_settings.MAIL_FROM,
        MAIL_PORT=email_settings.MAIL_PORT,
        MAIL_SERVER=email_settings.MAIL_SERVER,
        MAIL_FROM_NAME=email_settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=email_settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=email_settings.MAIL_SSL_TLS,
        USE_CREDENTIALS=email_settings.USE_CREDENTIALS,
        VALIDATE_CERTS=email_settings.VALIDATE_CERTS,
        TEMPLATE_FOLDER=os.path.join(os.path.dirname(__file__), "..", "templates", "email")
    )
