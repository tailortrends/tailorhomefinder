"""
Pydantic schemas for Agent management
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    """Agent account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"


class AgentRole(str, Enum):
    """Agent roles/levels"""
    JUNIOR_AGENT = "junior_agent"
    SENIOR_AGENT = "senior_agent"
    TEAM_LEAD = "team_lead"
    MANAGER = "manager"
    ADMIN = "admin"


class AgentBase(BaseModel):
    """Base agent schema"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    mobile: Optional[str] = Field(None, max_length=50)


class AgentCreate(AgentBase):
    """Schema for creating a new agent"""
    # Profile
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    title: Optional[str] = Field(None, max_length=100)

    # License
    license_number: Optional[str] = Field(None, max_length=50)
    license_state: Optional[str] = Field(None, max_length=50)
    license_expiry: Optional[datetime] = None

    # Specializations
    specializations: Optional[List[str]] = None
    service_areas: Optional[List[str]] = None
    languages: Optional[List[str]] = None

    # Status & Role
    status: AgentStatus = AgentStatus.ACTIVE
    role: AgentRole = AgentRole.JUNIOR_AGENT
    is_admin: bool = False

    # Capacity
    max_customers: int = Field(50, ge=1, le=500)

    # Schedule
    working_hours: Optional[Dict[str, str]] = None
    timezone: str = "America/New_York"

    # Commission
    commission_rate: Optional[float] = Field(None, ge=0, le=100)

    # Team
    manager_id: Optional[str] = None
    team_name: Optional[str] = None

    # Hired date
    hired_at: Optional[datetime] = None


class AgentUpdate(BaseModel):
    """Schema for updating agent info"""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    mobile: Optional[str] = Field(None, max_length=50)

    # Profile
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    title: Optional[str] = None

    # License
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    license_expiry: Optional[datetime] = None

    # Specializations
    specializations: Optional[List[str]] = None
    service_areas: Optional[List[str]] = None
    languages: Optional[List[str]] = None

    # Status & Role
    status: Optional[AgentStatus] = None
    role: Optional[AgentRole] = None
    is_admin: Optional[bool] = None

    # Capacity
    max_customers: Optional[int] = Field(None, ge=1, le=500)

    # Schedule
    working_hours: Optional[Dict[str, str]] = None
    timezone: Optional[str] = None

    # Commission
    commission_rate: Optional[float] = Field(None, ge=0, le=100)

    # Team
    manager_id: Optional[str] = None
    team_name: Optional[str] = None

    # Notes
    internal_notes: Optional[str] = None


class AgentResponse(BaseModel):
    """Schema for agent response"""
    id: str
    firebase_uid: Optional[str] = None
    email: str
    first_name: str
    last_name: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None

    # Profile
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    title: Optional[str] = None

    # License
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    license_expiry: Optional[datetime] = None

    # Specializations
    specializations: Optional[List[str]] = None
    service_areas: Optional[List[str]] = None
    languages: Optional[List[str]] = None

    # Status & Role
    status: str
    role: str
    is_admin: bool = False

    # Metrics
    total_customers: int = 0
    active_customers: int = 0
    closed_deals: int = 0
    rating: float = 0.0
    reviews_count: int = 0

    # Capacity
    max_customers: int = 50
    has_capacity: Optional[bool] = None

    # Schedule
    working_hours: Optional[Dict[str, str]] = None
    timezone: str = "America/New_York"

    # Commission
    commission_rate: Optional[float] = None

    # Team
    manager_id: Optional[str] = None
    team_name: Optional[str] = None

    # Activity
    last_login_at: Optional[datetime] = None
    last_active_at: Optional[datetime] = None

    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None
    hired_at: Optional[datetime] = None

    # Notes
    internal_notes: Optional[str] = None

    class Config:
        from_attributes = True


class AgentList(BaseModel):
    """Schema for paginated agent list"""
    total: int
    agents: List[AgentResponse]
    limit: int
    offset: int


class AgentStats(BaseModel):
    """Schema for agent statistics"""
    total_agents: int
    active_agents: int
    total_customers_managed: int
    avg_customers_per_agent: float
    total_closed_deals: int
    agents_by_status: dict
    agents_by_role: dict
    top_performers: List[dict]


class AgentAssignment(BaseModel):
    """Schema for assigning customer to agent"""
    customer_id: str
    agent_id: str
    notes: Optional[str] = None
