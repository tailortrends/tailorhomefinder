"""
User model for storing customer/user data
Links to Firebase Auth UID for authentication
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base
import enum
import uuid


class UserStatus(str, enum.Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class UserRole(str, enum.Enum):
    """User roles in the system"""
    CUSTOMER = "customer"
    AGENT = "agent"
    ADMIN = "admin"


class User(Base):
    """
    Model for storing user profile information.
    Links to Firebase Auth via firebase_uid.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Firebase Authentication Link
    firebase_uid = Column(String(128), unique=True, nullable=True, index=True)

    # Basic Info
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)

    # Profile Details
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)

    # Address
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(20), nullable=True)

    # Home Search Preferences (what they're looking for)
    preferred_locations = Column(JSON, nullable=True)  # List of cities/zip codes
    min_budget = Column(Integer, nullable=True)
    max_budget = Column(Integer, nullable=True)
    preferred_beds = Column(Integer, nullable=True)
    preferred_baths = Column(Float, nullable=True)
    preferred_sqft_min = Column(Integer, nullable=True)
    preferred_sqft_max = Column(Integer, nullable=True)
    preferred_property_types = Column(JSON, nullable=True)  # List of property types
    move_in_timeline = Column(String(100), nullable=True)  # ASAP, 1-3 months, etc.

    # Financial Info (optional)
    pre_approved = Column(Boolean, default=False)
    pre_approval_amount = Column(Integer, nullable=True)
    financing_type = Column(String(50), nullable=True)  # Cash, FHA, Conventional, VA

    # Status & Role
    status = Column(String(20), default=UserStatus.ACTIVE.value, index=True)
    role = Column(String(20), default=UserRole.CUSTOMER.value, index=True)

    # Assignment
    assigned_agent_id = Column(String, nullable=True, index=True)

    # Activity Tracking
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_active_at = Column(DateTime(timezone=True), nullable=True)
    search_count = Column(Integer, default=0)
    saved_properties_count = Column(Integer, default=0)
    inquiries_count = Column(Integer, default=0)

    # Communication Preferences
    email_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    marketing_emails = Column(Boolean, default=True)

    # Notes (for agents/admins)
    internal_notes = Column(Text, nullable=True)

    # Source tracking
    referral_source = Column(String(100), nullable=True)  # How they found us

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    interactions = relationship("CustomerInteraction", back_populates="customer", foreign_keys="CustomerInteraction.customer_id")
    notes = relationship("CustomerNote", back_populates="customer", foreign_keys="CustomerNote.customer_id")
    tasks = relationship("CustomerTask", back_populates="customer", foreign_keys="CustomerTask.customer_id")

    @property
    def full_name(self):
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.email

    @property
    def is_active(self):
        """Check if user is active"""
        return self.status == UserStatus.ACTIVE.value

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
