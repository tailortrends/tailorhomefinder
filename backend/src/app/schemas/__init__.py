"""
Pydantic schemas for TailorHomeFinder API
"""
from .property import (
    PropertyBase,
    PropertyCreate,
    PropertyResponse,
    PropertySearch,
    PropertyList
)
from .inquiry import (
    InquiryCreate,
    InquiryResponse,
    InquiryList,
    InquiryUpdateStatus,
    ContactFormSubmission,
    EmailResponse,
    InquiryType,
    InquiryStatus
)
from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserList,
    UserStats,
    UserActivityUpdate,
    UserStatus,
    UserRole
)
from .agent import (
    AgentBase,
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentList,
    AgentStats,
    AgentAssignment,
    AgentStatus,
    AgentRole
)
from .crm import (
    # Interaction
    InteractionCreate,
    InteractionUpdate,
    InteractionResponse,
    InteractionList,
    InteractionType,
    InteractionOutcome,
    # Note
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    NoteList,
    # Task
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskList,
    TaskPriority,
    TaskStatus,
    # Pipeline
    PipelineCreate,
    PipelineUpdate,
    PipelineResponse,
    PipelineList,
    PipelineStats,
    PipelineStage,
    # Feature Settings
    FeatureSettingCreate,
    FeatureSettingUpdate,
    FeatureSettingResponse,
    FeatureSettingList,
    FeatureToggle,
    # Activity Log
    ActivityLogCreate,
    ActivityLogResponse,
    ActivityLogList,
    # Dashboard Stats
    AdminDashboardStats,
    CRMDashboardStats
)

__all__ = [
    # Property schemas
    "PropertyBase",
    "PropertyCreate",
    "PropertyResponse",
    "PropertySearch",
    "PropertyList",
    # Inquiry schemas
    "InquiryCreate",
    "InquiryResponse",
    "InquiryList",
    "InquiryUpdateStatus",
    "ContactFormSubmission",
    "EmailResponse",
    "InquiryType",
    "InquiryStatus",
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserList",
    "UserStats",
    "UserActivityUpdate",
    "UserStatus",
    "UserRole",
    # Agent schemas
    "AgentBase",
    "AgentCreate",
    "AgentUpdate",
    "AgentResponse",
    "AgentList",
    "AgentStats",
    "AgentAssignment",
    "AgentStatus",
    "AgentRole",
    # CRM - Interaction
    "InteractionCreate",
    "InteractionUpdate",
    "InteractionResponse",
    "InteractionList",
    "InteractionType",
    "InteractionOutcome",
    # CRM - Note
    "NoteCreate",
    "NoteUpdate",
    "NoteResponse",
    "NoteList",
    # CRM - Task
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskList",
    "TaskPriority",
    "TaskStatus",
    # CRM - Pipeline
    "PipelineCreate",
    "PipelineUpdate",
    "PipelineResponse",
    "PipelineList",
    "PipelineStats",
    "PipelineStage",
    # Feature Settings
    "FeatureSettingCreate",
    "FeatureSettingUpdate",
    "FeatureSettingResponse",
    "FeatureSettingList",
    "FeatureToggle",
    # Activity Log
    "ActivityLogCreate",
    "ActivityLogResponse",
    "ActivityLogList",
    # Dashboard Stats
    "AdminDashboardStats",
    "CRMDashboardStats"
]
