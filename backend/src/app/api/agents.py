"""
Agent management API endpoints - Admin only
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional
from datetime import datetime
import uuid

from ..db.database import get_db
from ..models import Agent, AgentStatus, AgentRole, User
from ..schemas import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentList,
    AgentStats,
    AgentAssignment
)

router = APIRouter(prefix="/api/agents", tags=["Agents"])


@router.get("/", response_model=AgentList)
async def get_agents(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    role: Optional[str] = None,
    is_admin: Optional[bool] = None,
    search: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all agents with optional filters"""
    query = db.query(Agent)

    # Apply filters
    if status:
        query = query.filter(Agent.status == status)
    if role:
        query = query.filter(Agent.role == role)
    if is_admin is not None:
        query = query.filter(Agent.is_admin == is_admin)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Agent.email.ilike(search_term),
                Agent.first_name.ilike(search_term),
                Agent.last_name.ilike(search_term),
                Agent.phone.ilike(search_term)
            )
        )

    # Get total count
    total = query.count()

    # Apply pagination and ordering
    agents = query.order_by(Agent.created_at.desc()).offset(offset).limit(limit).all()

    # Convert to response with computed fields
    agent_responses = []
    for agent in agents:
        agent_dict = {
            **agent.__dict__,
            "full_name": agent.full_name,
            "has_capacity": agent.has_capacity
        }
        agent_responses.append(AgentResponse.model_validate(agent_dict))

    return AgentList(
        total=total,
        agents=agent_responses,
        limit=limit,
        offset=offset
    )


@router.get("/stats", response_model=AgentStats)
async def get_agent_stats(db: Session = Depends(get_db)):
    """Get agent statistics"""
    total = db.query(Agent).count()
    active = db.query(Agent).filter(Agent.status == AgentStatus.ACTIVE.value).count()

    # Total customers managed
    total_customers = db.query(func.sum(Agent.total_customers)).scalar() or 0

    # Average customers per agent
    avg_customers = (
        db.query(func.avg(Agent.active_customers))
        .filter(Agent.status == AgentStatus.ACTIVE.value)
        .scalar() or 0
    )

    # Total closed deals
    total_deals = db.query(func.sum(Agent.closed_deals)).scalar() or 0

    # Agents by status
    status_counts = db.query(
        Agent.status,
        func.count(Agent.id)
    ).group_by(Agent.status).all()
    agents_by_status = {status: count for status, count in status_counts}

    # Agents by role
    role_counts = db.query(
        Agent.role,
        func.count(Agent.id)
    ).group_by(Agent.role).all()
    agents_by_role = {role: count for role, count in role_counts}

    # Top performers (by closed deals)
    top_agents = (
        db.query(Agent)
        .filter(Agent.status == AgentStatus.ACTIVE.value)
        .order_by(Agent.closed_deals.desc())
        .limit(5)
        .all()
    )
    top_performers = [
        {
            "id": a.id,
            "name": a.full_name,
            "closed_deals": a.closed_deals,
            "rating": a.rating,
            "active_customers": a.active_customers
        }
        for a in top_agents
    ]

    return AgentStats(
        total_agents=total,
        active_agents=active,
        total_customers_managed=total_customers,
        avg_customers_per_agent=float(avg_customers),
        total_closed_deals=total_deals,
        agents_by_status=agents_by_status,
        agents_by_role=agents_by_role,
        top_performers=top_performers
    )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """Get agent by ID"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent_dict = {
        **agent.__dict__,
        "full_name": agent.full_name,
        "has_capacity": agent.has_capacity
    }
    return AgentResponse.model_validate(agent_dict)


@router.get("/firebase/{firebase_uid}", response_model=AgentResponse)
async def get_agent_by_firebase_uid(firebase_uid: str, db: Session = Depends(get_db)):
    """Get agent by Firebase UID"""
    agent = db.query(Agent).filter(Agent.firebase_uid == firebase_uid).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent_dict = {
        **agent.__dict__,
        "full_name": agent.full_name,
        "has_capacity": agent.has_capacity
    }
    return AgentResponse.model_validate(agent_dict)


@router.post("/", response_model=AgentResponse)
async def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent (Admin only)"""
    # Check if email already exists
    existing = db.query(Agent).filter(Agent.email == agent_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered as agent")

    agent = Agent(
        id=str(uuid.uuid4()),
        **agent_data.model_dump()
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    agent_dict = {
        **agent.__dict__,
        "full_name": agent.full_name,
        "has_capacity": agent.has_capacity
    }
    return AgentResponse.model_validate(agent_dict)


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db)
):
    """Update agent information (Admin only)"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Update fields
    for key, value in agent_data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(agent, key, value)

    db.commit()
    db.refresh(agent)

    agent_dict = {
        **agent.__dict__,
        "full_name": agent.full_name,
        "has_capacity": agent.has_capacity
    }
    return AgentResponse.model_validate(agent_dict)


@router.patch("/{agent_id}/status")
async def update_agent_status(
    agent_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    """Update agent status (Admin only)"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if status not in [s.value for s in AgentStatus]:
        raise HTTPException(status_code=400, detail="Invalid status")

    agent.status = status
    db.commit()

    return {"success": True, "status": status}


@router.patch("/{agent_id}/metrics")
async def update_agent_metrics(
    agent_id: str,
    total_customers: Optional[int] = None,
    active_customers: Optional[int] = None,
    closed_deals: Optional[int] = None,
    rating: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Update agent performance metrics"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if total_customers is not None:
        agent.total_customers = total_customers
    if active_customers is not None:
        agent.active_customers = active_customers
    if closed_deals is not None:
        agent.closed_deals = closed_deals
    if rating is not None:
        agent.rating = rating

    db.commit()

    return {"success": True}


@router.post("/assign-customer")
async def assign_customer_to_agent(
    assignment: AgentAssignment,
    db: Session = Depends(get_db)
):
    """Assign a customer to an agent"""
    # Verify agent exists and is active
    agent = db.query(Agent).filter(Agent.id == assignment.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.status != AgentStatus.ACTIVE.value:
        raise HTTPException(status_code=400, detail="Agent is not active")
    if not agent.has_capacity:
        raise HTTPException(status_code=400, detail="Agent is at capacity")

    # Verify customer exists
    customer = db.query(User).filter(User.id == assignment.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Assign customer
    customer.assigned_agent_id = assignment.agent_id

    # Update agent metrics
    agent.active_customers = (agent.active_customers or 0) + 1
    agent.total_customers = (agent.total_customers or 0) + 1

    db.commit()

    return {
        "success": True,
        "customer_id": assignment.customer_id,
        "agent_id": assignment.agent_id,
        "agent_name": agent.full_name
    }


@router.get("/{agent_id}/customers", response_model=dict)
async def get_agent_customers(
    agent_id: str,
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all customers assigned to an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    query = db.query(User).filter(User.assigned_agent_id == agent_id)
    total = query.count()
    customers = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "total": total,
        "customers": [
            {
                "id": c.id,
                "email": c.email,
                "full_name": c.full_name,
                "phone": c.phone,
                "status": c.status,
                "created_at": c.created_at
            }
            for c in customers
        ],
        "limit": limit,
        "offset": offset
    }


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    """Delete an agent (soft delete - sets status to terminated)"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Soft delete
    agent.status = AgentStatus.TERMINATED.value
    db.commit()

    return {"success": True, "message": "Agent terminated"}
