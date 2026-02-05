"""
Admin API endpoints - Dashboard stats, feature settings, activity logs
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional
from datetime import datetime, timedelta
import uuid

from ..db.database import get_db
from ..models import (
    User,
    Agent,
    Inquiry,
    Property,
    CustomerPipeline,
    FeatureSettings,
    ActivityLog,
    UserStatus,
    AgentStatus,
    InquiryStatus,
    PipelineStage
)
from ..schemas import (
    AdminDashboardStats,
    FeatureSettingCreate,
    FeatureSettingUpdate,
    FeatureSettingResponse,
    FeatureSettingList,
    FeatureToggle,
    ActivityLogCreate,
    ActivityLogResponse,
    ActivityLogList
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# ================== Dashboard Stats ==================

@router.get("/stats", response_model=AdminDashboardStats)
async def get_admin_dashboard_stats(db: Session = Depends(get_db)):
    """Get admin dashboard overview statistics"""
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # User stats
    total_customers = db.query(User).filter(User.role == "customer").count()
    active_customers = db.query(User).filter(
        and_(User.role == "customer", User.status == UserStatus.ACTIVE.value)
    ).count()

    # Agent stats
    total_agents = db.query(Agent).count()
    active_agents = db.query(Agent).filter(
        Agent.status == AgentStatus.ACTIVE.value
    ).count()

    # Inquiry stats
    total_inquiries = db.query(Inquiry).count()
    new_inquiries = db.query(Inquiry).filter(
        Inquiry.status == InquiryStatus.NEW.value
    ).count()

    # Property stats
    total_properties = db.query(Property).count()
    # For properties_viewed, we'd need a views table - using 0 for now
    properties_viewed = 0

    # Pipeline stats this month
    leads_this_month = db.query(CustomerPipeline).filter(
        CustomerPipeline.created_at >= month_start
    ).count()

    conversions_this_month = db.query(CustomerPipeline).filter(
        and_(
            CustomerPipeline.stage == PipelineStage.CLOSED_WON.value,
            CustomerPipeline.last_stage_change >= month_start
        )
    ).count()

    # Revenue this month (sum of deal values for closed deals)
    revenue = db.query(func.sum(CustomerPipeline.deal_value)).filter(
        and_(
            CustomerPipeline.stage == PipelineStage.CLOSED_WON.value,
            CustomerPipeline.last_stage_change >= month_start
        )
    ).scalar()

    return AdminDashboardStats(
        total_customers=total_customers,
        active_customers=active_customers,
        total_agents=total_agents,
        active_agents=active_agents,
        total_inquiries=total_inquiries,
        new_inquiries=new_inquiries,
        total_properties=total_properties,
        properties_viewed=properties_viewed,
        leads_this_month=leads_this_month,
        conversions_this_month=conversions_this_month,
        revenue_this_month=revenue
    )


# ================== Feature Settings ==================

@router.get("/features", response_model=FeatureSettingList)
async def get_feature_settings(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    is_enabled: Optional[bool] = None
):
    """Get all feature settings"""
    query = db.query(FeatureSettings)

    if category:
        query = query.filter(FeatureSettings.category == category)
    if is_enabled is not None:
        query = query.filter(FeatureSettings.is_enabled == is_enabled)

    features = query.order_by(FeatureSettings.display_order, FeatureSettings.feature_key).all()

    return FeatureSettingList(
        total=len(features),
        features=[FeatureSettingResponse.model_validate(f) for f in features]
    )


@router.get("/features/{feature_key}", response_model=FeatureSettingResponse)
async def get_feature_setting(feature_key: str, db: Session = Depends(get_db)):
    """Get single feature setting by key"""
    feature = db.query(FeatureSettings).filter(
        FeatureSettings.feature_key == feature_key
    ).first()
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    return FeatureSettingResponse.model_validate(feature)


@router.post("/features", response_model=FeatureSettingResponse)
async def create_feature_setting(
    data: FeatureSettingCreate,
    db: Session = Depends(get_db)
):
    """Create a new feature setting"""
    existing = db.query(FeatureSettings).filter(
        FeatureSettings.feature_key == data.feature_key
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Feature key already exists")

    feature = FeatureSettings(
        id=str(uuid.uuid4()),
        **data.model_dump()
    )

    db.add(feature)
    db.commit()
    db.refresh(feature)

    return FeatureSettingResponse.model_validate(feature)


@router.patch("/features/{feature_key}", response_model=FeatureSettingResponse)
async def update_feature_setting(
    feature_key: str,
    data: FeatureSettingUpdate,
    db: Session = Depends(get_db)
):
    """Update a feature setting"""
    feature = db.query(FeatureSettings).filter(
        FeatureSettings.feature_key == feature_key
    ).first()
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(feature, key, value)

    db.commit()
    db.refresh(feature)

    return FeatureSettingResponse.model_validate(feature)


@router.patch("/features/{feature_key}/toggle", response_model=FeatureSettingResponse)
async def toggle_feature(
    feature_key: str,
    toggle: FeatureToggle,
    db: Session = Depends(get_db)
):
    """Toggle a feature on/off"""
    feature = db.query(FeatureSettings).filter(
        FeatureSettings.feature_key == feature_key
    ).first()
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    feature.is_enabled = toggle.is_enabled
    feature.enabled_by = toggle.enabled_by
    feature.enabled_at = datetime.utcnow()

    db.commit()
    db.refresh(feature)

    return FeatureSettingResponse.model_validate(feature)


@router.delete("/features/{feature_key}")
async def delete_feature_setting(feature_key: str, db: Session = Depends(get_db)):
    """Delete a feature setting"""
    feature = db.query(FeatureSettings).filter(
        FeatureSettings.feature_key == feature_key
    ).first()
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    db.delete(feature)
    db.commit()
    return {"success": True}


@router.post("/features/seed")
async def seed_default_features(db: Session = Depends(get_db)):
    """Seed default feature settings"""
    default_features = [
        {
            "feature_key": "dashboard_saved_properties",
            "feature_name": "Saved Properties",
            "description": "Show saved properties section on user dashboard",
            "category": "dashboard",
            "is_enabled": True,
            "display_order": 1
        },
        {
            "feature_key": "dashboard_recent_searches",
            "feature_name": "Recent Searches",
            "description": "Show recent searches section on user dashboard",
            "category": "dashboard",
            "is_enabled": True,
            "display_order": 2
        },
        {
            "feature_key": "dashboard_recommendations",
            "feature_name": "Property Recommendations",
            "description": "Show AI-powered property recommendations",
            "category": "dashboard",
            "is_enabled": True,
            "display_order": 3
        },
        {
            "feature_key": "dashboard_price_alerts",
            "feature_name": "Price Alerts",
            "description": "Allow users to set price alerts for properties",
            "category": "dashboard",
            "is_enabled": True,
            "display_order": 4
        },
        {
            "feature_key": "dashboard_market_stats",
            "feature_name": "Market Statistics",
            "description": "Show local market statistics and trends",
            "category": "dashboard",
            "is_enabled": True,
            "display_order": 5
        },
        {
            "feature_key": "search_advanced_filters",
            "feature_name": "Advanced Search Filters",
            "description": "Enable advanced search filters",
            "category": "search",
            "is_enabled": True,
            "display_order": 1
        },
        {
            "feature_key": "search_map_view",
            "feature_name": "Map View",
            "description": "Enable map view in search results",
            "category": "search",
            "is_enabled": True,
            "display_order": 2
        },
        {
            "feature_key": "property_comparison",
            "feature_name": "Property Comparison",
            "description": "Allow users to compare properties side by side",
            "category": "property",
            "is_enabled": True,
            "display_order": 1
        },
        {
            "feature_key": "property_virtual_tour",
            "feature_name": "Virtual Tours",
            "description": "Enable virtual property tours",
            "category": "property",
            "is_enabled": True,
            "display_order": 2
        },
        {
            "feature_key": "property_mortgage_calculator",
            "feature_name": "Mortgage Calculator",
            "description": "Show mortgage calculator on property pages",
            "category": "property",
            "is_enabled": True,
            "display_order": 3
        },
        {
            "feature_key": "contact_schedule_tour",
            "feature_name": "Schedule Tours",
            "description": "Allow users to schedule property tours",
            "category": "contact",
            "is_enabled": True,
            "display_order": 1
        },
        {
            "feature_key": "contact_chat_agent",
            "feature_name": "Live Chat",
            "description": "Enable live chat with agents",
            "category": "contact",
            "is_enabled": False,
            "display_order": 2
        }
    ]

    created = 0
    for feature_data in default_features:
        existing = db.query(FeatureSettings).filter(
            FeatureSettings.feature_key == feature_data["feature_key"]
        ).first()
        if not existing:
            feature = FeatureSettings(
                id=str(uuid.uuid4()),
                **feature_data
            )
            db.add(feature)
            created += 1

    db.commit()
    return {"success": True, "created": created}


# ================== Activity Logs ==================

@router.get("/activity", response_model=ActivityLogList)
async def get_activity_logs(
    db: Session = Depends(get_db),
    actor_id: Optional[str] = None,
    actor_type: Optional[str] = None,
    action: Optional[str] = None,
    action_category: Optional[str] = None,
    target_type: Optional[str] = None,
    target_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """Get activity logs with filters"""
    query = db.query(ActivityLog)

    if actor_id:
        query = query.filter(ActivityLog.actor_id == actor_id)
    if actor_type:
        query = query.filter(ActivityLog.actor_type == actor_type)
    if action:
        query = query.filter(ActivityLog.action == action)
    if action_category:
        query = query.filter(ActivityLog.action_category == action_category)
    if target_type:
        query = query.filter(ActivityLog.target_type == target_type)
    if target_id:
        query = query.filter(ActivityLog.target_id == target_id)

    total = query.count()
    activities = query.order_by(ActivityLog.created_at.desc()).offset(offset).limit(limit).all()

    return ActivityLogList(
        total=total,
        activities=[ActivityLogResponse.model_validate(a) for a in activities],
        limit=limit,
        offset=offset
    )


@router.post("/activity", response_model=ActivityLogResponse)
async def create_activity_log(
    data: ActivityLogCreate,
    db: Session = Depends(get_db)
):
    """Create a new activity log entry"""
    activity = ActivityLog(
        id=str(uuid.uuid4()),
        **data.model_dump()
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return ActivityLogResponse.model_validate(activity)


@router.get("/activity/recent")
async def get_recent_activity(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=50)
):
    """Get recent activity for admin dashboard"""
    activities = (
        db.query(ActivityLog)
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "activities": [
            {
                "id": a.id,
                "actor_email": a.actor_email,
                "action": a.action,
                "description": a.description,
                "target_type": a.target_type,
                "created_at": a.created_at
            }
            for a in activities
        ]
    }
