"""
API endpoints for property inquiries and contact form submissions
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from datetime import datetime
import logging

from ..db.database import get_db
from ..models.inquiry import Inquiry, InquiryType as ModelInquiryType, InquiryStatus as ModelInquiryStatus
from ..models.property import Property
from ..schemas.inquiry import (
    InquiryCreate,
    InquiryResponse,
    InquiryList,
    InquiryUpdateStatus,
    ContactFormSubmission,
    EmailResponse,
    InquiryStatus,
    InquiryType
)
from ..services.email_service import send_inquiry_emails

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/inquiries", tags=["inquiries"])


def map_inquiry_type(frontend_type: Optional[str]) -> ModelInquiryType:
    """Map frontend inquiry type to model enum"""
    type_map = {
        "general": ModelInquiryType.GENERAL,
        "schedule_tour": ModelInquiryType.SCHEDULE_TOUR,
        "request_info": ModelInquiryType.REQUEST_INFO,
        "make_offer": ModelInquiryType.MAKE_OFFER
    }
    return type_map.get(frontend_type, ModelInquiryType.GENERAL)


@router.post("/contact", response_model=EmailResponse)
async def submit_contact_form(
    submission: ContactFormSubmission,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submit a contact form inquiry for a property

    This endpoint:
    1. Creates an inquiry record in the database
    2. Sends notification email to admin/agent (background)
    3. Sends confirmation email to the inquirer (background)
    """
    try:
        # Get property details if available
        property_data = None
        agent_email = None
        property_address = submission.propertyAddress
        property_price = submission.propertyPrice

        if submission.propertyId:
            property_data = db.query(Property).filter(Property.id == submission.propertyId).first()
            if property_data:
                property_address = property_address or property_data.address
                property_price = property_price or property_data.price
                # Could get agent email from property if available
                # agent_email = property_data.agent_email

        # Determine inquiry type from message content if not specified
        inquiry_type = submission.inquiryType or InquiryType.GENERAL
        message_lower = submission.message.lower()
        if "tour" in message_lower or "schedule" in message_lower or "visit" in message_lower:
            inquiry_type = InquiryType.SCHEDULE_TOUR
        elif "offer" in message_lower:
            inquiry_type = InquiryType.MAKE_OFFER

        # Create inquiry record
        inquiry = Inquiry(
            name=submission.name,
            email=submission.email,
            phone=submission.phone,
            message=submission.message,
            inquiry_type=map_inquiry_type(inquiry_type.value if inquiry_type else "general"),
            property_id=submission.propertyId,
            property_address=property_address,
            property_price=property_price,
            agent_email=agent_email,
            status=ModelInquiryStatus.NEW
        )

        db.add(inquiry)
        db.commit()
        db.refresh(inquiry)

        logger.info(f"Created inquiry {inquiry.id} from {submission.email}")

        # Send emails in background
        background_tasks.add_task(
            send_inquiry_emails,
            inquiry_id=inquiry.id,
            name=submission.name,
            email=submission.email,
            phone=submission.phone,
            message=submission.message,
            inquiry_type=inquiry_type.value if inquiry_type else "general",
            property_address=property_address,
            property_price=property_price,
            agent_email=agent_email
        )

        # Update inquiry to mark email as sent
        background_tasks.add_task(
            mark_email_sent,
            db=db,
            inquiry_id=inquiry.id
        )

        return EmailResponse(
            success=True,
            message="Your inquiry has been submitted successfully. We'll be in touch soon!",
            inquiry_id=inquiry.id
        )

    except Exception as e:
        logger.error(f"Failed to process inquiry: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to process your inquiry. Please try again later."
        )


async def mark_email_sent(db: Session, inquiry_id: str):
    """Background task to mark email as sent"""
    try:
        inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
        if inquiry:
            inquiry.email_sent = True
            inquiry.email_sent_at = datetime.utcnow()
            db.commit()
    except Exception as e:
        logger.error(f"Failed to mark email sent for inquiry {inquiry_id}: {str(e)}")


@router.get("/", response_model=InquiryList)
async def list_inquiries(
    status: Optional[InquiryStatus] = None,
    property_id: Optional[str] = None,
    limit: int = Query(default=20, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List all inquiries with optional filtering

    - Filter by status (new, read, responded, closed)
    - Filter by property_id
    - Pagination support
    """
    query = db.query(Inquiry)

    # Apply filters
    if status:
        query = query.filter(Inquiry.status == ModelInquiryStatus[status.value.upper()])

    if property_id:
        query = query.filter(Inquiry.property_id == property_id)

    # Get total count
    total = query.count()

    # Apply pagination and ordering
    inquiries = query.order_by(desc(Inquiry.created_at)).offset(offset).limit(limit).all()

    return InquiryList(
        total=total,
        inquiries=[InquiryResponse.model_validate(inq) for inq in inquiries],
        limit=limit,
        offset=offset
    )


@router.get("/{inquiry_id}", response_model=InquiryResponse)
async def get_inquiry(inquiry_id: str, db: Session = Depends(get_db)):
    """Get a specific inquiry by ID"""
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()

    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    return InquiryResponse.model_validate(inquiry)


@router.patch("/{inquiry_id}/status", response_model=InquiryResponse)
async def update_inquiry_status(
    inquiry_id: str,
    status_update: InquiryUpdateStatus,
    db: Session = Depends(get_db)
):
    """Update the status of an inquiry"""
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()

    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    inquiry.status = ModelInquiryStatus[status_update.status.value.upper()]
    db.commit()
    db.refresh(inquiry)

    return InquiryResponse.model_validate(inquiry)


@router.get("/stats/overview")
async def get_inquiry_stats(db: Session = Depends(get_db)):
    """Get inquiry statistics for the admin dashboard"""
    total = db.query(Inquiry).count()
    new_count = db.query(Inquiry).filter(Inquiry.status == ModelInquiryStatus.NEW).count()
    responded_count = db.query(Inquiry).filter(Inquiry.status == ModelInquiryStatus.RESPONDED).count()

    # Count by type
    tour_requests = db.query(Inquiry).filter(
        Inquiry.inquiry_type == ModelInquiryType.SCHEDULE_TOUR
    ).count()
    offer_inquiries = db.query(Inquiry).filter(
        Inquiry.inquiry_type == ModelInquiryType.MAKE_OFFER
    ).count()

    return {
        "total_inquiries": total,
        "new_inquiries": new_count,
        "responded_inquiries": responded_count,
        "tour_requests": tour_requests,
        "offer_inquiries": offer_inquiries
    }
