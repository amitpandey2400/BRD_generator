"""
API routes for projects
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional, Dict

from storage.database import get_db
from storage.models import Project, ProjectStatus
from brd_generator.orchestrator import BRDOrchestrator
from sqlalchemy import select

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = ""


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    created_at: str
    
    class Config:
        from_attributes = True


class IngestRequest(BaseModel):
    sources: Dict


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new project"""
    orchestrator = BRDOrchestrator(db)
    project = await orchestrator.create_project(
        name=project_data.name,
        description=project_data.description
    )
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        status=project.status.value,
        created_at=project.created_at.isoformat()
    )


@router.get("", response_model=List[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    """List all projects"""
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    projects = result.scalars().all()
    
    return [
        ProjectResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            status=p.status.value,
            created_at=p.created_at.isoformat()
        )
        for p in projects
    ]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get project details"""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        status=project.status.value,
        created_at=project.created_at.isoformat()
    )


@router.post("/{project_id}/ingest")
async def ingest_data(
    project_id: str,
    request: IngestRequest,
    db: AsyncSession = Depends(get_db)
):
    """Trigger data ingestion for a project"""
    orchestrator = BRDOrchestrator(db)
    
    try:
        result = await orchestrator.ingest_data(project_id, request.sources)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_id}/process")
async def process_data(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Process ingested data and extract requirements"""
    orchestrator = BRDOrchestrator(db)
    
    try:
        result = await orchestrator.process_and_extract(project_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_id}/generate-brd")
async def generate_brd(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Generate BRD for a project"""
    orchestrator = BRDOrchestrator(db)
    
    try:
        brd = await orchestrator.generate_brd(project_id)
        return {
            "brd_id": brd.id,
            "project_id": project_id,
            "status": "generated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a project"""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await db.delete(project)
    await db.commit()
    
    return {"message": "Project deleted successfully"}
