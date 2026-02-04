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
    "InquiryStatus"
]
