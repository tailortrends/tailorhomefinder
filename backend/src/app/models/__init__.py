"""
SQLAlchemy models for TailorHomeFinder
"""
from .property import Property
from .inquiry import Inquiry, InquiryType, InquiryStatus
from .user import User, UserStatus, UserRole
from .agent import Agent, AgentStatus, AgentRole
from .crm import (
    CustomerInteraction,
    CustomerNote,
    CustomerTask,
    CustomerPipeline,
    FeatureSettings,
    ActivityLog,
    InteractionType,
    InteractionOutcome,
    TaskPriority,
    TaskStatus,
    PipelineStage
)

__all__ = [
    # Property
    "Property",
    # Inquiry
    "Inquiry",
    "InquiryType",
    "InquiryStatus",
    # User
    "User",
    "UserStatus",
    "UserRole",
    # Agent
    "Agent",
    "AgentStatus",
    "AgentRole",
    # CRM
    "CustomerInteraction",
    "CustomerNote",
    "CustomerTask",
    "CustomerPipeline",
    "FeatureSettings",
    "ActivityLog",
    "InteractionType",
    "InteractionOutcome",
    "TaskPriority",
    "TaskStatus",
    "PipelineStage"
]
