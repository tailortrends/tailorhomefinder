"""
Agent model for staff members who manage customers
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base
import enum
import uuid


class AgentStatus(str, enum.Enum):
    """Agent account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"


class AgentRole(str, enum.Enum):
    """Agent roles/levels"""
    JUNIOR_AGENT = "junior_agent"
    SENIOR_AGENT = "senior_agent"
    TEAM_LEAD = "team_lead"
    MANAGER = "manager"
    ADMIN = "admin"


class Agent(Base):
    """
    Model for agents/staff who manage customers.
    Only admins can create/manage agents.
    """
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Firebase Authentication Link (for agent login)
    firebase_uid = Column(String(128), unique=True, nullable=True, index=True)

    # Basic Info
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=True)
    mobile = Column(String(50), nullable=True)

    # Profile
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    title = Column(String(100), nullable=True)  # e.g., "Senior Real Estate Agent"

    # License Info
    license_number = Column(String(50), nullable=True)
    license_state = Column(String(50), nullable=True)
    license_expiry = Column(DateTime(timezone=True), nullable=True)

    # Specializations
    specializations = Column(JSON, nullable=True)  # e.g., ["Luxury", "First-time buyers", "Commercial"]
    service_areas = Column(JSON, nullable=True)  # List of cities/regions they cover
    languages = Column(JSON, nullable=True)  # Languages spoken

    # Status & Role
    status = Column(String(20), default=AgentStatus.ACTIVE.value, index=True)
    role = Column(String(20), default=AgentRole.JUNIOR_AGENT.value, index=True)
    is_admin = Column(Boolean, default=False, index=True)

    # Performance Metrics
    total_customers = Column(Integer, default=0)
    active_customers = Column(Integer, default=0)
    closed_deals = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)

    # Capacity
    max_customers = Column(Integer, default=50)  # Max customers they can handle

    # Schedule
    working_hours = Column(JSON, nullable=True)  # {"monday": "9:00-17:00", etc.}
    timezone = Column(String(50), default="America/New_York")

    # Commission (for internal tracking)
    commission_rate = Column(Float, nullable=True)

    # Manager/Team
    manager_id = Column(String, nullable=True, index=True)  # Reports to
    team_name = Column(String(100), nullable=True)

    # Last Activity
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_active_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    hired_at = Column(DateTime(timezone=True), nullable=True)

    # Internal Notes (admin only)
    internal_notes = Column(Text, nullable=True)

    # Relationships
    interactions = relationship("CustomerInteraction", back_populates="agent", foreign_keys="CustomerInteraction.agent_id")
    notes = relationship("CustomerNote", back_populates="agent", foreign_keys="CustomerNote.agent_id")
    tasks = relationship("CustomerTask", back_populates="assigned_agent", foreign_keys="CustomerTask.assigned_agent_id")

    @property
    def full_name(self):
        """Get full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        """Check if agent is active"""
        return self.status == AgentStatus.ACTIVE.value

    @property
    def has_capacity(self):
        """Check if agent can take more customers"""
        return self.active_customers < self.max_customers

    def __repr__(self):
        return f"<Agent(id={self.id}, name={self.full_name}, role={self.role})>"
