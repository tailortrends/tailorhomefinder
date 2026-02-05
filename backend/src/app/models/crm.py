"""
CRM models for customer relationship management
Includes interactions, notes, tasks, and pipeline stages
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base
import enum
import uuid


class InteractionType(str, enum.Enum):
    """Types of customer interactions"""
    PHONE_CALL = "phone_call"
    EMAIL = "email"
    SMS = "sms"
    IN_PERSON = "in_person"
    VIDEO_CALL = "video_call"
    PROPERTY_TOUR = "property_tour"
    OPEN_HOUSE = "open_house"
    DOCUMENT_SENT = "document_sent"
    OFFER_SUBMITTED = "offer_submitted"
    CONTRACT_SIGNED = "contract_signed"
    OTHER = "other"


class InteractionOutcome(str, enum.Enum):
    """Outcome of an interaction"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    FOLLOW_UP_NEEDED = "follow_up_needed"
    NO_ANSWER = "no_answer"
    LEFT_VOICEMAIL = "left_voicemail"


class TaskPriority(str, enum.Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, enum.Enum):
    """Task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


class PipelineStage(str, enum.Enum):
    """Customer pipeline stages"""
    NEW_LEAD = "new_lead"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    VIEWING_PROPERTIES = "viewing_properties"
    MAKING_OFFERS = "making_offers"
    UNDER_CONTRACT = "under_contract"
    CLOSING = "closing"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    ON_HOLD = "on_hold"


class CustomerInteraction(Base):
    """
    Track all interactions with customers.
    Used for CRM and relationship management.
    """
    __tablename__ = "customer_interactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # References
    customer_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=True, index=True)
    property_id = Column(String, ForeignKey("properties.id"), nullable=True, index=True)

    # Interaction Details
    interaction_type = Column(
        SQLEnum(InteractionType, name="interaction_type_enum"),
        default=InteractionType.OTHER,
        nullable=False,
        index=True
    )
    subject = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    outcome = Column(
        SQLEnum(InteractionOutcome, name="interaction_outcome_enum"),
        default=InteractionOutcome.NEUTRAL,
        nullable=True
    )

    # Duration (for calls/meetings)
    duration_minutes = Column(Integer, nullable=True)

    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Follow-up
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
    follow_up_notes = Column(Text, nullable=True)

    # Attachments (URLs to documents)
    attachments = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("User", back_populates="interactions", foreign_keys=[customer_id])
    agent = relationship("Agent", back_populates="interactions", foreign_keys=[agent_id])

    def __repr__(self):
        return f"<CustomerInteraction(id={self.id}, type={self.interaction_type}, customer={self.customer_id})>"


class CustomerNote(Base):
    """
    Internal notes about customers.
    Not visible to customers, only to agents/admins.
    """
    __tablename__ = "customer_notes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # References
    customer_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=True, index=True)

    # Note Content
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)

    # Categorization
    category = Column(String(50), nullable=True)  # e.g., "preferences", "concerns", "timeline"
    is_pinned = Column(Boolean, default=False)
    is_important = Column(Boolean, default=False)

    # Visibility
    is_private = Column(Boolean, default=False)  # Only visible to creator

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("User", back_populates="notes", foreign_keys=[customer_id])
    agent = relationship("Agent", back_populates="notes", foreign_keys=[agent_id])

    def __repr__(self):
        return f"<CustomerNote(id={self.id}, customer={self.customer_id})>"


class CustomerTask(Base):
    """
    Tasks related to customers.
    For agents to track follow-ups and action items.
    """
    __tablename__ = "customer_tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # References
    customer_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    assigned_agent_id = Column(String, ForeignKey("agents.id"), nullable=True, index=True)
    created_by_agent_id = Column(String, ForeignKey("agents.id"), nullable=True)
    property_id = Column(String, ForeignKey("properties.id"), nullable=True, index=True)

    # Task Details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Priority & Status
    priority = Column(
        SQLEnum(TaskPriority, name="task_priority_enum"),
        default=TaskPriority.MEDIUM,
        nullable=False,
        index=True
    )
    status = Column(
        SQLEnum(TaskStatus, name="task_status_enum"),
        default=TaskStatus.PENDING,
        nullable=False,
        index=True
    )

    # Scheduling
    due_date = Column(DateTime(timezone=True), nullable=True, index=True)
    reminder_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Category
    task_type = Column(String(50), nullable=True)  # e.g., "follow_up", "document", "showing"

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("User", back_populates="tasks", foreign_keys=[customer_id])
    assigned_agent = relationship("Agent", back_populates="tasks", foreign_keys=[assigned_agent_id])

    def __repr__(self):
        return f"<CustomerTask(id={self.id}, title={self.title}, status={self.status})>"


class CustomerPipeline(Base):
    """
    Track customer progress through the sales pipeline.
    Shows where each customer is in their home-buying journey.
    """
    __tablename__ = "customer_pipeline"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Customer Reference
    customer_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    assigned_agent_id = Column(String, ForeignKey("agents.id"), nullable=True, index=True)

    # Pipeline Stage
    stage = Column(
        SQLEnum(PipelineStage, name="pipeline_stage_enum"),
        default=PipelineStage.NEW_LEAD,
        nullable=False,
        index=True
    )
    previous_stage = Column(String(50), nullable=True)

    # Stage Timestamps
    stage_entered_at = Column(DateTime(timezone=True), server_default=func.now())
    last_stage_change = Column(DateTime(timezone=True), nullable=True)

    # Deal Info
    expected_close_date = Column(DateTime(timezone=True), nullable=True)
    deal_value = Column(Integer, nullable=True)  # Expected transaction value
    probability = Column(Integer, default=0)  # 0-100% probability of closing

    # Lost Deal Info
    lost_reason = Column(String(255), nullable=True)
    lost_to_competitor = Column(String(255), nullable=True)

    # Source
    lead_source = Column(String(100), nullable=True)  # Website, Referral, etc.

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<CustomerPipeline(customer={self.customer_id}, stage={self.stage})>"


class FeatureSettings(Base):
    """
    Feature toggle settings for the user dashboard.
    Admins can enable/disable features that appear on user dashboards.
    """
    __tablename__ = "feature_settings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Feature identification
    feature_key = Column(String(100), unique=True, nullable=False, index=True)
    feature_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Toggle
    is_enabled = Column(Boolean, default=True, index=True)

    # Categorization
    category = Column(String(50), nullable=True)  # e.g., "search", "dashboard", "profile"

    # Display order
    display_order = Column(Integer, default=0)

    # Access Level
    min_role = Column(String(20), default="customer")  # Minimum role to see this feature

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    enabled_by = Column(String, nullable=True)  # Agent/Admin who last toggled
    enabled_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<FeatureSettings(key={self.feature_key}, enabled={self.is_enabled})>"


class ActivityLog(Base):
    """
    Log of all admin/agent activities for audit trail.
    """
    __tablename__ = "activity_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Actor
    actor_id = Column(String, nullable=False, index=True)
    actor_type = Column(String(20), nullable=False)  # "agent", "admin", "system"
    actor_email = Column(String(255), nullable=True)

    # Action
    action = Column(String(100), nullable=False, index=True)
    action_category = Column(String(50), nullable=True)  # "user", "agent", "settings", etc.
    description = Column(Text, nullable=True)

    # Target
    target_type = Column(String(50), nullable=True)  # "user", "agent", "property", etc.
    target_id = Column(String, nullable=True, index=True)

    # Details
    details = Column(JSON, nullable=True)  # Additional context
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ActivityLog(actor={self.actor_id}, action={self.action})>"
