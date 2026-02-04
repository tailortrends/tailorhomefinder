"""
Pydantic schemas for inquiry/contact form submissions
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class InquiryType(str, Enum):
    """Types of inquiries"""
    GENERAL = "general"
    SCHEDULE_TOUR = "schedule_tour"
    REQUEST_INFO = "request_info"
    MAKE_OFFER = "make_offer"


class InquiryStatus(str, Enum):
    """Status of an inquiry"""
    NEW = "new"
    READ = "read"
    RESPONDED = "responded"
    CLOSED = "closed"


class InquiryCreate(BaseModel):
    """Schema for creating a new inquiry"""
    name: str = Field(..., min_length=2, max_length=255, description="Full name of the inquirer")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    message: str = Field(..., min_length=10, max_length=2000, description="Inquiry message")
    inquiry_type: InquiryType = Field(default=InquiryType.GENERAL, description="Type of inquiry")

    # Property Information
    property_id: str = Field(..., description="ID of the property being inquired about")
    property_address: Optional[str] = Field(None, max_length=500, description="Property address for reference")
    property_price: Optional[int] = Field(None, ge=0, description="Property price")

    # Agent routing (optional)
    agent_email: Optional[EmailStr] = Field(None, description="Agent email to notify")


class InquiryResponse(BaseModel):
    """Schema for inquiry response"""
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    inquiry_type: InquiryType
    property_id: Optional[str] = None
    property_address: Optional[str] = None
    property_price: Optional[int] = None
    status: InquiryStatus
    email_sent: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InquiryList(BaseModel):
    """Schema for list of inquiries"""
    total: int
    inquiries: list[InquiryResponse]
    limit: int
    offset: int


class InquiryUpdateStatus(BaseModel):
    """Schema for updating inquiry status"""
    status: InquiryStatus


class ContactFormSubmission(BaseModel):
    """Schema for frontend contact form submission"""
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=50)
    message: str = Field(..., min_length=10, max_length=2000)
    propertyId: str = Field(..., alias="property_id")
    propertyAddress: Optional[str] = Field(None, alias="property_address")
    propertyPrice: Optional[int] = Field(None, alias="property_price")
    inquiryType: Optional[InquiryType] = Field(default=InquiryType.GENERAL, alias="inquiry_type")

    class Config:
        populate_by_name = True


class EmailNotificationRequest(BaseModel):
    """Schema for sending email notifications"""
    to_email: EmailStr
    subject: str
    template_name: str
    template_data: dict


class EmailResponse(BaseModel):
    """Schema for email send response"""
    success: bool
    message: str
    inquiry_id: Optional[str] = None
