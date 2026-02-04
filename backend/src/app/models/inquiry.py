"""
Inquiry model for storing contact form submissions
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from ..db.database import Base
import enum
import uuid


class InquiryType(str, enum.Enum):
    """Types of inquiries"""
    GENERAL = "general"
    SCHEDULE_TOUR = "schedule_tour"
    REQUEST_INFO = "request_info"
    MAKE_OFFER = "make_offer"


class InquiryStatus(str, enum.Enum):
    """Status of an inquiry"""
    NEW = "new"
    READ = "read"
    RESPONDED = "responded"
    CLOSED = "closed"


class Inquiry(Base):
    """Model for storing property inquiries/contact submissions"""

    __tablename__ = "inquiries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Contact Information
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=True)

    # Inquiry Details
    message = Column(Text, nullable=False)
    inquiry_type = Column(
        SQLEnum(InquiryType, name="inquiry_type_enum"),
        default=InquiryType.GENERAL,
        nullable=False
    )

    # Property Reference
    property_id = Column(String, ForeignKey("properties.id"), nullable=True, index=True)
    property_address = Column(String(500), nullable=True)
    property_price = Column(Integer, nullable=True)

    # Agent Information (for routing)
    agent_name = Column(String(255), nullable=True)
    agent_email = Column(String(255), nullable=True)

    # Status Tracking
    status = Column(
        SQLEnum(InquiryStatus, name="inquiry_status_enum"),
        default=InquiryStatus.NEW,
        nullable=False,
        index=True
    )

    # Email Tracking
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Inquiry(id={self.id}, email={self.email}, property_id={self.property_id})>"
