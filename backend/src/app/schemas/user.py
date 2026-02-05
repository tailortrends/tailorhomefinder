"""
Pydantic schemas for User management
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class UserRole(str, Enum):
    """User roles in the system"""
    CUSTOMER = "customer"
    AGENT = "agent"
    ADMIN = "admin"


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    firebase_uid: Optional[str] = Field(None, max_length=128)
    role: UserRole = UserRole.CUSTOMER
    status: UserStatus = UserStatus.ACTIVE

    # Profile Details
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    # Address
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

    # Search Preferences
    preferred_locations: Optional[List[str]] = None
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None
    preferred_beds: Optional[int] = None
    preferred_baths: Optional[float] = None
    preferred_sqft_min: Optional[int] = None
    preferred_sqft_max: Optional[int] = None
    preferred_property_types: Optional[List[str]] = None
    move_in_timeline: Optional[str] = None

    # Financial
    pre_approved: bool = False
    pre_approval_amount: Optional[int] = None
    financing_type: Optional[str] = None

    # Communication
    email_notifications: bool = True
    sms_notifications: bool = False
    marketing_emails: bool = True

    # Source
    referral_source: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating user info"""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)

    # Profile Details
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    # Address
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

    # Search Preferences
    preferred_locations: Optional[List[str]] = None
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None
    preferred_beds: Optional[int] = None
    preferred_baths: Optional[float] = None
    preferred_sqft_min: Optional[int] = None
    preferred_sqft_max: Optional[int] = None
    preferred_property_types: Optional[List[str]] = None
    move_in_timeline: Optional[str] = None

    # Financial
    pre_approved: Optional[bool] = None
    pre_approval_amount: Optional[int] = None
    financing_type: Optional[str] = None

    # Status
    status: Optional[UserStatus] = None

    # Assignment
    assigned_agent_id: Optional[str] = None

    # Communication
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    marketing_emails: Optional[bool] = None

    # Internal (admin only)
    internal_notes: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    id: str
    firebase_uid: Optional[str] = None
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None

    # Profile
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    # Address
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

    # Preferences
    preferred_locations: Optional[List[str]] = None
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None
    preferred_beds: Optional[int] = None
    preferred_baths: Optional[float] = None
    preferred_sqft_min: Optional[int] = None
    preferred_sqft_max: Optional[int] = None
    preferred_property_types: Optional[List[str]] = None
    move_in_timeline: Optional[str] = None

    # Financial
    pre_approved: bool = False
    pre_approval_amount: Optional[int] = None
    financing_type: Optional[str] = None

    # Status
    status: str
    role: str

    # Assignment
    assigned_agent_id: Optional[str] = None

    # Activity
    last_login_at: Optional[datetime] = None
    last_active_at: Optional[datetime] = None
    search_count: int = 0
    saved_properties_count: int = 0
    inquiries_count: int = 0

    # Communication
    email_notifications: bool = True
    sms_notifications: bool = False
    marketing_emails: bool = True

    # Notes
    internal_notes: Optional[str] = None
    referral_source: Optional[str] = None

    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserList(BaseModel):
    """Schema for paginated user list"""
    total: int
    users: List[UserResponse]
    limit: int
    offset: int


class UserStats(BaseModel):
    """Schema for user statistics"""
    total_users: int
    active_users: int
    inactive_users: int
    new_users_today: int
    new_users_this_week: int
    new_users_this_month: int
    users_by_status: dict
    users_by_role: dict


class UserActivityUpdate(BaseModel):
    """Schema for updating user activity"""
    last_login_at: Optional[datetime] = None
    last_active_at: Optional[datetime] = None
    search_count: Optional[int] = None
    saved_properties_count: Optional[int] = None
    inquiries_count: Optional[int] = None
