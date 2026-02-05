"""
User management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional
from datetime import datetime, timedelta
import uuid

from ..db.database import get_db
from ..models import User, UserStatus, UserRole
from ..schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserList,
    UserStats,
    UserActivityUpdate
)

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=UserList)
async def get_users(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    role: Optional[str] = None,
    assigned_agent_id: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all users with optional filters"""
    query = db.query(User)

    # Apply filters
    if status:
        query = query.filter(User.status == status)
    if role:
        query = query.filter(User.role == role)
    if assigned_agent_id:
        query = query.filter(User.assigned_agent_id == assigned_agent_id)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                User.email.ilike(search_term),
                User.first_name.ilike(search_term),
                User.last_name.ilike(search_term),
                User.phone.ilike(search_term)
            )
        )

    # Get total count
    total = query.count()

    # Apply pagination and ordering
    users = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()

    # Convert to response with full_name
    user_responses = []
    for user in users:
        user_dict = {
            **user.__dict__,
            "full_name": user.full_name
        }
        user_responses.append(UserResponse.model_validate(user_dict))

    return UserList(
        total=total,
        users=user_responses,
        limit=limit,
        offset=offset
    )


@router.get("/stats", response_model=UserStats)
async def get_user_stats(db: Session = Depends(get_db)):
    """Get user statistics"""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=now.weekday())
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    total = db.query(User).count()
    active = db.query(User).filter(User.status == UserStatus.ACTIVE.value).count()
    inactive = db.query(User).filter(User.status == UserStatus.INACTIVE.value).count()

    new_today = db.query(User).filter(User.created_at >= today_start).count()
    new_week = db.query(User).filter(User.created_at >= week_start).count()
    new_month = db.query(User).filter(User.created_at >= month_start).count()

    # Users by status
    status_counts = db.query(
        User.status,
        func.count(User.id)
    ).group_by(User.status).all()
    users_by_status = {status: count for status, count in status_counts}

    # Users by role
    role_counts = db.query(
        User.role,
        func.count(User.id)
    ).group_by(User.role).all()
    users_by_role = {role: count for role, count in role_counts}

    return UserStats(
        total_users=total,
        active_users=active,
        inactive_users=inactive,
        new_users_today=new_today,
        new_users_this_week=new_week,
        new_users_this_month=new_month,
        users_by_status=users_by_status,
        users_by_role=users_by_role
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = {**user.__dict__, "full_name": user.full_name}
    return UserResponse.model_validate(user_dict)


@router.get("/firebase/{firebase_uid}", response_model=UserResponse)
async def get_user_by_firebase_uid(firebase_uid: str, db: Session = Depends(get_db)):
    """Get user by Firebase UID"""
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = {**user.__dict__, "full_name": user.full_name}
    return UserResponse.model_validate(user_dict)


@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if email already exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if firebase_uid already exists
    if user_data.firebase_uid:
        existing_firebase = db.query(User).filter(
            User.firebase_uid == user_data.firebase_uid
        ).first()
        if existing_firebase:
            raise HTTPException(status_code=400, detail="Firebase UID already registered")

    user = User(
        id=str(uuid.uuid4()),
        **user_data.model_dump()
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    user_dict = {**user.__dict__, "full_name": user.full_name}
    return UserResponse.model_validate(user_dict)


@router.post("/sync", response_model=UserResponse)
async def sync_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Sync user from Firebase - create if not exists, update if exists"""
    existing = None

    # First try to find by firebase_uid
    if user_data.firebase_uid:
        existing = db.query(User).filter(
            User.firebase_uid == user_data.firebase_uid
        ).first()

    # If not found by firebase_uid, try email
    if not existing:
        existing = db.query(User).filter(User.email == user_data.email).first()

    if existing:
        # Update existing user
        for key, value in user_data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(existing, key, value)
        existing.last_login_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        user_dict = {**existing.__dict__, "full_name": existing.full_name}
        return UserResponse.model_validate(user_dict)
    else:
        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            **user_data.model_dump()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user_dict = {**user.__dict__, "full_name": user.full_name}
        return UserResponse.model_validate(user_dict)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update user information"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields
    for key, value in user_data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    user_dict = {**user.__dict__, "full_name": user.full_name}
    return UserResponse.model_validate(user_dict)


@router.patch("/{user_id}/status")
async def update_user_status(
    user_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    """Update user status (active/inactive/suspended)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if status not in [s.value for s in UserStatus]:
        raise HTTPException(status_code=400, detail="Invalid status")

    user.status = status
    db.commit()

    return {"success": True, "status": status}


@router.patch("/{user_id}/assign-agent")
async def assign_agent_to_user(
    user_id: str,
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Assign an agent to a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.assigned_agent_id = agent_id
    db.commit()

    return {"success": True, "assigned_agent_id": agent_id}


@router.patch("/{user_id}/activity", response_model=UserResponse)
async def update_user_activity(
    user_id: str,
    activity: UserActivityUpdate,
    db: Session = Depends(get_db)
):
    """Update user activity metrics"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in activity.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    user_dict = {**user.__dict__, "full_name": user.full_name}
    return UserResponse.model_validate(user_dict)


@router.delete("/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete a user (soft delete - sets status to inactive)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Soft delete - just set status to inactive
    user.status = UserStatus.INACTIVE.value
    db.commit()

    return {"success": True, "message": "User deactivated"}
