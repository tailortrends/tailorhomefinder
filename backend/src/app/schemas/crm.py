"""
Pydantic schemas for CRM functionality
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class InteractionType(str, Enum):
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


class InteractionOutcome(str, Enum):
    """Outcome of an interaction"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    FOLLOW_UP_NEEDED = "follow_up_needed"
    NO_ANSWER = "no_answer"
    LEFT_VOICEMAIL = "left_voicemail"


class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, Enum):
    """Task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


class PipelineStage(str, Enum):
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


# ================== Interaction Schemas ==================

class InteractionCreate(BaseModel):
    """Schema for creating an interaction"""
    customer_id: str
    agent_id: Optional[str] = None
    property_id: Optional[str] = None

    interaction_type: InteractionType = InteractionType.OTHER
    subject: Optional[str] = Field(None, max_length=255)
    description: str = Field(..., min_length=1)
    outcome: Optional[InteractionOutcome] = InteractionOutcome.NEUTRAL

    duration_minutes: Optional[int] = Field(None, ge=0)
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None
    follow_up_notes: Optional[str] = None

    attachments: Optional[List[str]] = None


class InteractionUpdate(BaseModel):
    """Schema for updating an interaction"""
    subject: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    outcome: Optional[InteractionOutcome] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    completed_at: Optional[datetime] = None
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[datetime] = None
    follow_up_notes: Optional[str] = None
    attachments: Optional[List[str]] = None


class InteractionResponse(BaseModel):
    """Schema for interaction response"""
    id: str
    customer_id: str
    agent_id: Optional[str] = None
    property_id: Optional[str] = None

    interaction_type: InteractionType
    subject: Optional[str] = None
    description: str
    outcome: Optional[InteractionOutcome] = None

    duration_minutes: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None
    follow_up_notes: Optional[str] = None

    attachments: Optional[List[str]] = None

    created_at: datetime
    updated_at: Optional[datetime] = None

    # Populated relationships
    customer_name: Optional[str] = None
    agent_name: Optional[str] = None

    class Config:
        from_attributes = True


class InteractionList(BaseModel):
    """Schema for interaction list"""
    total: int
    interactions: List[InteractionResponse]
    limit: int
    offset: int


# ================== Note Schemas ==================

class NoteCreate(BaseModel):
    """Schema for creating a note"""
    customer_id: str
    agent_id: Optional[str] = None
    title: Optional[str] = Field(None, max_length=255)
    content: str = Field(..., min_length=1)
    category: Optional[str] = Field(None, max_length=50)
    is_pinned: bool = False
    is_important: bool = False
    is_private: bool = False


class NoteUpdate(BaseModel):
    """Schema for updating a note"""
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    category: Optional[str] = None
    is_pinned: Optional[bool] = None
    is_important: Optional[bool] = None
    is_private: Optional[bool] = None


class NoteResponse(BaseModel):
    """Schema for note response"""
    id: str
    customer_id: str
    agent_id: Optional[str] = None
    title: Optional[str] = None
    content: str
    category: Optional[str] = None
    is_pinned: bool = False
    is_important: bool = False
    is_private: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Populated
    agent_name: Optional[str] = None

    class Config:
        from_attributes = True


class NoteList(BaseModel):
    """Schema for note list"""
    total: int
    notes: List[NoteResponse]
    limit: int
    offset: int


# ================== Task Schemas ==================

class TaskCreate(BaseModel):
    """Schema for creating a task"""
    customer_id: Optional[str] = None
    assigned_agent_id: Optional[str] = None
    property_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    task_type: Optional[str] = Field(None, max_length=50)


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    assigned_agent_id: Optional[str] = None
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    task_type: Optional[str] = None


class TaskResponse(BaseModel):
    """Schema for task response"""
    id: str
    customer_id: Optional[str] = None
    assigned_agent_id: Optional[str] = None
    property_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    priority: TaskPriority
    status: TaskStatus
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    task_type: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Populated
    customer_name: Optional[str] = None
    assigned_agent_name: Optional[str] = None

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    """Schema for task list"""
    total: int
    tasks: List[TaskResponse]
    limit: int
    offset: int


# ================== Pipeline Schemas ==================

class PipelineCreate(BaseModel):
    """Schema for creating pipeline entry"""
    customer_id: str
    assigned_agent_id: Optional[str] = None
    stage: PipelineStage = PipelineStage.NEW_LEAD
    expected_close_date: Optional[datetime] = None
    deal_value: Optional[int] = Field(None, ge=0)
    probability: int = Field(0, ge=0, le=100)
    lead_source: Optional[str] = Field(None, max_length=100)


class PipelineUpdate(BaseModel):
    """Schema for updating pipeline"""
    stage: Optional[PipelineStage] = None
    assigned_agent_id: Optional[str] = None
    expected_close_date: Optional[datetime] = None
    deal_value: Optional[int] = Field(None, ge=0)
    probability: Optional[int] = Field(None, ge=0, le=100)
    lost_reason: Optional[str] = None
    lost_to_competitor: Optional[str] = None


class PipelineResponse(BaseModel):
    """Schema for pipeline response"""
    id: str
    customer_id: str
    assigned_agent_id: Optional[str] = None
    stage: PipelineStage
    previous_stage: Optional[str] = None
    stage_entered_at: datetime
    last_stage_change: Optional[datetime] = None
    expected_close_date: Optional[datetime] = None
    deal_value: Optional[int] = None
    probability: int = 0
    lost_reason: Optional[str] = None
    lost_to_competitor: Optional[str] = None
    lead_source: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Populated
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    assigned_agent_name: Optional[str] = None

    class Config:
        from_attributes = True


class PipelineList(BaseModel):
    """Schema for pipeline list"""
    total: int
    pipelines: List[PipelineResponse]
    limit: int
    offset: int


class PipelineStats(BaseModel):
    """Schema for pipeline statistics"""
    total_leads: int
    leads_by_stage: dict
    total_deal_value: int
    avg_deal_value: float
    conversion_rate: float
    avg_time_to_close: Optional[float] = None


# ================== Feature Settings Schemas ==================

class FeatureSettingCreate(BaseModel):
    """Schema for creating feature setting"""
    feature_key: str = Field(..., min_length=1, max_length=100)
    feature_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_enabled: bool = True
    category: Optional[str] = Field(None, max_length=50)
    display_order: int = 0
    min_role: str = "customer"


class FeatureSettingUpdate(BaseModel):
    """Schema for updating feature setting"""
    feature_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_enabled: Optional[bool] = None
    category: Optional[str] = None
    display_order: Optional[int] = None
    min_role: Optional[str] = None


class FeatureSettingResponse(BaseModel):
    """Schema for feature setting response"""
    id: str
    feature_key: str
    feature_name: str
    description: Optional[str] = None
    is_enabled: bool = True
    category: Optional[str] = None
    display_order: int = 0
    min_role: str = "customer"
    created_at: datetime
    updated_at: Optional[datetime] = None
    enabled_by: Optional[str] = None
    enabled_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FeatureSettingList(BaseModel):
    """Schema for feature settings list"""
    total: int
    features: List[FeatureSettingResponse]


class FeatureToggle(BaseModel):
    """Schema for toggling a feature"""
    is_enabled: bool
    enabled_by: Optional[str] = None


# ================== Activity Log Schemas ==================

class ActivityLogCreate(BaseModel):
    """Schema for creating activity log"""
    actor_id: str
    actor_type: str
    actor_email: Optional[str] = None
    action: str
    action_category: Optional[str] = None
    description: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    details: Optional[dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class ActivityLogResponse(BaseModel):
    """Schema for activity log response"""
    id: str
    actor_id: str
    actor_type: str
    actor_email: Optional[str] = None
    action: str
    action_category: Optional[str] = None
    description: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    details: Optional[dict] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityLogList(BaseModel):
    """Schema for activity log list"""
    total: int
    activities: List[ActivityLogResponse]
    limit: int
    offset: int


# ================== Dashboard Stats Schemas ==================

class AdminDashboardStats(BaseModel):
    """Schema for admin dashboard overview stats"""
    total_customers: int
    active_customers: int
    total_agents: int
    active_agents: int
    total_inquiries: int
    new_inquiries: int
    total_properties: int
    properties_viewed: int
    leads_this_month: int
    conversions_this_month: int
    revenue_this_month: Optional[int] = None


class CRMDashboardStats(BaseModel):
    """Schema for CRM dashboard stats"""
    total_interactions: int
    interactions_today: int
    pending_tasks: int
    overdue_tasks: int
    follow_ups_due: int
    pipeline_value: int
    customers_in_pipeline: int
