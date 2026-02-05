"""
CRM API endpoints - Interactions, Notes, Tasks, Pipeline
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional
from datetime import datetime, timedelta
import uuid

from ..db.database import get_db
from ..models import (
    CustomerInteraction,
    CustomerNote,
    CustomerTask,
    CustomerPipeline,
    User,
    Agent,
    InteractionType,
    TaskStatus,
    TaskPriority,
    PipelineStage
)
from ..schemas import (
    # Interaction
    InteractionCreate,
    InteractionUpdate,
    InteractionResponse,
    InteractionList,
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
    # Pipeline
    PipelineCreate,
    PipelineUpdate,
    PipelineResponse,
    PipelineList,
    PipelineStats,
    # Dashboard
    CRMDashboardStats
)

router = APIRouter(prefix="/api/crm", tags=["CRM"])


# ================== Interactions ==================

@router.get("/interactions", response_model=InteractionList)
async def get_interactions(
    db: Session = Depends(get_db),
    customer_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    interaction_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get customer interactions with filters"""
    query = db.query(CustomerInteraction)

    if customer_id:
        query = query.filter(CustomerInteraction.customer_id == customer_id)
    if agent_id:
        query = query.filter(CustomerInteraction.agent_id == agent_id)
    if interaction_type:
        query = query.filter(CustomerInteraction.interaction_type == interaction_type)

    total = query.count()
    interactions = query.order_by(CustomerInteraction.created_at.desc()).offset(offset).limit(limit).all()

    # Populate names
    interaction_responses = []
    for i in interactions:
        customer = db.query(User).filter(User.id == i.customer_id).first()
        agent = db.query(Agent).filter(Agent.id == i.agent_id).first() if i.agent_id else None

        resp = InteractionResponse(
            **i.__dict__,
            customer_name=customer.full_name if customer else None,
            agent_name=agent.full_name if agent else None
        )
        interaction_responses.append(resp)

    return InteractionList(
        total=total,
        interactions=interaction_responses,
        limit=limit,
        offset=offset
    )


@router.get("/interactions/{interaction_id}", response_model=InteractionResponse)
async def get_interaction(interaction_id: str, db: Session = Depends(get_db)):
    """Get single interaction by ID"""
    interaction = db.query(CustomerInteraction).filter(
        CustomerInteraction.id == interaction_id
    ).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    customer = db.query(User).filter(User.id == interaction.customer_id).first()
    agent = db.query(Agent).filter(Agent.id == interaction.agent_id).first() if interaction.agent_id else None

    return InteractionResponse(
        **interaction.__dict__,
        customer_name=customer.full_name if customer else None,
        agent_name=agent.full_name if agent else None
    )


@router.post("/interactions", response_model=InteractionResponse)
async def create_interaction(
    data: InteractionCreate,
    db: Session = Depends(get_db)
):
    """Create a new interaction"""
    interaction = CustomerInteraction(
        id=str(uuid.uuid4()),
        **data.model_dump()
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    customer = db.query(User).filter(User.id == interaction.customer_id).first()
    agent = db.query(Agent).filter(Agent.id == interaction.agent_id).first() if interaction.agent_id else None

    return InteractionResponse(
        **interaction.__dict__,
        customer_name=customer.full_name if customer else None,
        agent_name=agent.full_name if agent else None
    )


@router.patch("/interactions/{interaction_id}", response_model=InteractionResponse)
async def update_interaction(
    interaction_id: str,
    data: InteractionUpdate,
    db: Session = Depends(get_db)
):
    """Update an interaction"""
    interaction = db.query(CustomerInteraction).filter(
        CustomerInteraction.id == interaction_id
    ).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(interaction, key, value)

    db.commit()
    db.refresh(interaction)

    customer = db.query(User).filter(User.id == interaction.customer_id).first()
    agent = db.query(Agent).filter(Agent.id == interaction.agent_id).first() if interaction.agent_id else None

    return InteractionResponse(
        **interaction.__dict__,
        customer_name=customer.full_name if customer else None,
        agent_name=agent.full_name if agent else None
    )


@router.delete("/interactions/{interaction_id}")
async def delete_interaction(interaction_id: str, db: Session = Depends(get_db)):
    """Delete an interaction"""
    interaction = db.query(CustomerInteraction).filter(
        CustomerInteraction.id == interaction_id
    ).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    db.delete(interaction)
    db.commit()
    return {"success": True}


# ================== Notes ==================

@router.get("/notes", response_model=NoteList)
async def get_notes(
    db: Session = Depends(get_db),
    customer_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    category: Optional[str] = None,
    is_pinned: Optional[bool] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get customer notes with filters"""
    query = db.query(CustomerNote)

    if customer_id:
        query = query.filter(CustomerNote.customer_id == customer_id)
    if agent_id:
        query = query.filter(CustomerNote.agent_id == agent_id)
    if category:
        query = query.filter(CustomerNote.category == category)
    if is_pinned is not None:
        query = query.filter(CustomerNote.is_pinned == is_pinned)

    total = query.count()

    # Order pinned first, then by date
    notes = (
        query
        .order_by(CustomerNote.is_pinned.desc(), CustomerNote.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    note_responses = []
    for n in notes:
        agent = db.query(Agent).filter(Agent.id == n.agent_id).first() if n.agent_id else None
        resp = NoteResponse(
            **n.__dict__,
            agent_name=agent.full_name if agent else None
        )
        note_responses.append(resp)

    return NoteList(
        total=total,
        notes=note_responses,
        limit=limit,
        offset=offset
    )


@router.post("/notes", response_model=NoteResponse)
async def create_note(data: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note"""
    note = CustomerNote(
        id=str(uuid.uuid4()),
        **data.model_dump()
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    agent = db.query(Agent).filter(Agent.id == note.agent_id).first() if note.agent_id else None

    return NoteResponse(
        **note.__dict__,
        agent_name=agent.full_name if agent else None
    )


@router.patch("/notes/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    data: NoteUpdate,
    db: Session = Depends(get_db)
):
    """Update a note"""
    note = db.query(CustomerNote).filter(CustomerNote.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(note, key, value)

    db.commit()
    db.refresh(note)

    agent = db.query(Agent).filter(Agent.id == note.agent_id).first() if note.agent_id else None

    return NoteResponse(
        **note.__dict__,
        agent_name=agent.full_name if agent else None
    )


@router.delete("/notes/{note_id}")
async def delete_note(note_id: str, db: Session = Depends(get_db)):
    """Delete a note"""
    note = db.query(CustomerNote).filter(CustomerNote.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"success": True}


# ================== Tasks ==================

@router.get("/tasks", response_model=TaskList)
async def get_tasks(
    db: Session = Depends(get_db),
    customer_id: Optional[str] = None,
    assigned_agent_id: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_before: Optional[datetime] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get tasks with filters"""
    query = db.query(CustomerTask)

    if customer_id:
        query = query.filter(CustomerTask.customer_id == customer_id)
    if assigned_agent_id:
        query = query.filter(CustomerTask.assigned_agent_id == assigned_agent_id)
    if status:
        query = query.filter(CustomerTask.status == status)
    if priority:
        query = query.filter(CustomerTask.priority == priority)
    if due_before:
        query = query.filter(CustomerTask.due_date <= due_before)

    total = query.count()
    tasks = query.order_by(CustomerTask.due_date.asc().nullslast(), CustomerTask.priority.desc()).offset(offset).limit(limit).all()

    task_responses = []
    for t in tasks:
        customer = db.query(User).filter(User.id == t.customer_id).first() if t.customer_id else None
        agent = db.query(Agent).filter(Agent.id == t.assigned_agent_id).first() if t.assigned_agent_id else None

        resp = TaskResponse(
            **t.__dict__,
            customer_name=customer.full_name if customer else None,
            assigned_agent_name=agent.full_name if agent else None
        )
        task_responses.append(resp)

    return TaskList(
        total=total,
        tasks=task_responses,
        limit=limit,
        offset=offset
    )


@router.get("/tasks/overdue", response_model=TaskList)
async def get_overdue_tasks(
    db: Session = Depends(get_db),
    assigned_agent_id: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get overdue tasks"""
    now = datetime.utcnow()
    query = db.query(CustomerTask).filter(
        and_(
            CustomerTask.due_date < now,
            CustomerTask.status.in_([TaskStatus.PENDING.value, TaskStatus.IN_PROGRESS.value])
        )
    )

    if assigned_agent_id:
        query = query.filter(CustomerTask.assigned_agent_id == assigned_agent_id)

    total = query.count()
    tasks = query.order_by(CustomerTask.due_date.asc()).offset(offset).limit(limit).all()

    task_responses = []
    for t in tasks:
        customer = db.query(User).filter(User.id == t.customer_id).first() if t.customer_id else None
        agent = db.query(Agent).filter(Agent.id == t.assigned_agent_id).first() if t.assigned_agent_id else None

        resp = TaskResponse(
            **t.__dict__,
            customer_name=customer.full_name if customer else None,
            assigned_agent_name=agent.full_name if agent else None
        )
        task_responses.append(resp)

    return TaskList(
        total=total,
        tasks=task_responses,
        limit=limit,
        offset=offset
    )


@router.post("/tasks", response_model=TaskResponse)
async def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    task = CustomerTask(
        id=str(uuid.uuid4()),
        **data.model_dump()
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    customer = db.query(User).filter(User.id == task.customer_id).first() if task.customer_id else None
    agent = db.query(Agent).filter(Agent.id == task.assigned_agent_id).first() if task.assigned_agent_id else None

    return TaskResponse(
        **task.__dict__,
        customer_name=customer.full_name if customer else None,
        assigned_agent_name=agent.full_name if agent else None
    )


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a task"""
    task = db.query(CustomerTask).filter(CustomerTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(task, key, value)

    # Auto-set completed_at when status changes to completed
    if data.status == TaskStatus.COMPLETED and not task.completed_at:
        task.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    customer = db.query(User).filter(User.id == task.customer_id).first() if task.customer_id else None
    agent = db.query(Agent).filter(Agent.id == task.assigned_agent_id).first() if task.assigned_agent_id else None

    return TaskResponse(
        **task.__dict__,
        customer_name=customer.full_name if customer else None,
        assigned_agent_name=agent.full_name if agent else None
    )


@router.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: str, db: Session = Depends(get_db)):
    """Mark a task as completed"""
    task = db.query(CustomerTask).filter(CustomerTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = TaskStatus.COMPLETED.value
    task.completed_at = datetime.utcnow()
    db.commit()

    return {"success": True}


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """Delete a task"""
    task = db.query(CustomerTask).filter(CustomerTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"success": True}


# ================== Pipeline ==================

@router.get("/pipeline", response_model=PipelineList)
async def get_pipeline(
    db: Session = Depends(get_db),
    stage: Optional[str] = None,
    assigned_agent_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """Get pipeline entries"""
    query = db.query(CustomerPipeline)

    if stage:
        query = query.filter(CustomerPipeline.stage == stage)
    if assigned_agent_id:
        query = query.filter(CustomerPipeline.assigned_agent_id == assigned_agent_id)

    total = query.count()
    pipelines = query.order_by(CustomerPipeline.stage_entered_at.desc()).offset(offset).limit(limit).all()

    pipeline_responses = []
    for p in pipelines:
        customer = db.query(User).filter(User.id == p.customer_id).first()
        agent = db.query(Agent).filter(Agent.id == p.assigned_agent_id).first() if p.assigned_agent_id else None

        resp = PipelineResponse(
            **p.__dict__,
            customer_name=customer.full_name if customer else None,
            customer_email=customer.email if customer else None,
            assigned_agent_name=agent.full_name if agent else None
        )
        pipeline_responses.append(resp)

    return PipelineList(
        total=total,
        pipelines=pipeline_responses,
        limit=limit,
        offset=offset
    )


@router.get("/pipeline/stats", response_model=PipelineStats)
async def get_pipeline_stats(db: Session = Depends(get_db)):
    """Get pipeline statistics"""
    total = db.query(CustomerPipeline).count()

    # Leads by stage
    stage_counts = db.query(
        CustomerPipeline.stage,
        func.count(CustomerPipeline.id)
    ).group_by(CustomerPipeline.stage).all()
    leads_by_stage = {stage: count for stage, count in stage_counts}

    # Total deal value
    total_value = db.query(func.sum(CustomerPipeline.deal_value)).scalar() or 0

    # Average deal value
    avg_value = db.query(func.avg(CustomerPipeline.deal_value)).scalar() or 0

    # Conversion rate (closed won / total that reached closing stages)
    closed_won = db.query(CustomerPipeline).filter(
        CustomerPipeline.stage == PipelineStage.CLOSED_WON.value
    ).count()
    closed_total = db.query(CustomerPipeline).filter(
        CustomerPipeline.stage.in_([
            PipelineStage.CLOSED_WON.value,
            PipelineStage.CLOSED_LOST.value
        ])
    ).count()
    conversion_rate = (closed_won / closed_total * 100) if closed_total > 0 else 0

    return PipelineStats(
        total_leads=total,
        leads_by_stage=leads_by_stage,
        total_deal_value=total_value,
        avg_deal_value=float(avg_value),
        conversion_rate=float(conversion_rate)
    )


@router.post("/pipeline", response_model=PipelineResponse)
async def create_pipeline_entry(data: PipelineCreate, db: Session = Depends(get_db)):
    """Create a new pipeline entry for a customer"""
    # Check if customer already has pipeline entry
    existing = db.query(CustomerPipeline).filter(
        CustomerPipeline.customer_id == data.customer_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer already in pipeline")

    pipeline = CustomerPipeline(
        id=str(uuid.uuid4()),
        **data.model_dump()
    )

    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)

    customer = db.query(User).filter(User.id == pipeline.customer_id).first()
    agent = db.query(Agent).filter(Agent.id == pipeline.assigned_agent_id).first() if pipeline.assigned_agent_id else None

    return PipelineResponse(
        **pipeline.__dict__,
        customer_name=customer.full_name if customer else None,
        customer_email=customer.email if customer else None,
        assigned_agent_name=agent.full_name if agent else None
    )


@router.patch("/pipeline/{pipeline_id}", response_model=PipelineResponse)
async def update_pipeline(
    pipeline_id: str,
    data: PipelineUpdate,
    db: Session = Depends(get_db)
):
    """Update pipeline entry"""
    pipeline = db.query(CustomerPipeline).filter(
        CustomerPipeline.id == pipeline_id
    ).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline entry not found")

    # Track stage changes
    if data.stage and data.stage.value != pipeline.stage:
        pipeline.previous_stage = pipeline.stage
        pipeline.last_stage_change = datetime.utcnow()
        pipeline.stage_entered_at = datetime.utcnow()

    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            if hasattr(value, 'value'):  # Handle enums
                setattr(pipeline, key, value.value)
            else:
                setattr(pipeline, key, value)

    db.commit()
    db.refresh(pipeline)

    customer = db.query(User).filter(User.id == pipeline.customer_id).first()
    agent = db.query(Agent).filter(Agent.id == pipeline.assigned_agent_id).first() if pipeline.assigned_agent_id else None

    return PipelineResponse(
        **pipeline.__dict__,
        customer_name=customer.full_name if customer else None,
        customer_email=customer.email if customer else None,
        assigned_agent_name=agent.full_name if agent else None
    )


@router.patch("/pipeline/customer/{customer_id}/stage")
async def update_customer_pipeline_stage(
    customer_id: str,
    stage: str,
    db: Session = Depends(get_db)
):
    """Update pipeline stage by customer ID"""
    pipeline = db.query(CustomerPipeline).filter(
        CustomerPipeline.customer_id == customer_id
    ).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Customer not in pipeline")

    if stage not in [s.value for s in PipelineStage]:
        raise HTTPException(status_code=400, detail="Invalid stage")

    pipeline.previous_stage = pipeline.stage
    pipeline.stage = stage
    pipeline.last_stage_change = datetime.utcnow()
    pipeline.stage_entered_at = datetime.utcnow()

    db.commit()

    return {"success": True, "stage": stage}


# ================== Dashboard Stats ==================

@router.get("/stats", response_model=CRMDashboardStats)
async def get_crm_stats(db: Session = Depends(get_db)):
    """Get CRM dashboard statistics"""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    total_interactions = db.query(CustomerInteraction).count()
    interactions_today = db.query(CustomerInteraction).filter(
        CustomerInteraction.created_at >= today_start
    ).count()

    pending_tasks = db.query(CustomerTask).filter(
        CustomerTask.status == TaskStatus.PENDING.value
    ).count()

    overdue_tasks = db.query(CustomerTask).filter(
        and_(
            CustomerTask.due_date < now,
            CustomerTask.status.in_([TaskStatus.PENDING.value, TaskStatus.IN_PROGRESS.value])
        )
    ).count()

    # Follow-ups due (interactions with follow_up_required and date passed)
    follow_ups_due = db.query(CustomerInteraction).filter(
        and_(
            CustomerInteraction.follow_up_required == True,
            CustomerInteraction.follow_up_date <= now
        )
    ).count()

    # Pipeline value
    pipeline_value = db.query(func.sum(CustomerPipeline.deal_value)).scalar() or 0
    customers_in_pipeline = db.query(CustomerPipeline).filter(
        CustomerPipeline.stage.notin_([
            PipelineStage.CLOSED_WON.value,
            PipelineStage.CLOSED_LOST.value
        ])
    ).count()

    return CRMDashboardStats(
        total_interactions=total_interactions,
        interactions_today=interactions_today,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks,
        follow_ups_due=follow_ups_due,
        pipeline_value=pipeline_value,
        customers_in_pipeline=customers_in_pipeline
    )
