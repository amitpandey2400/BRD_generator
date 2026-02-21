"""
API routes for BRDs
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import select

from storage.database import get_db
from storage.models import BRD, Citation, Requirement
from brd_generator.editor import BRDEditor
from brd_generator.orchestrator import BRDOrchestrator

router = APIRouter()


class BRDResponse(BaseModel):
    id: str
    project_id: str
    version: int
    title: str
    executive_summary: Optional[str]
    full_document: str
    created_at: str
    
    class Config:
        from_attributes = True


class EditRequest(BaseModel):
    edit_request: str
    section: Optional[str] = None


class GenerateRequest(BaseModel):
    project_id: str


class CitationResponse(BaseModel):
    requirement_id: str
    requirement_title: str
    data_source_id: str
    source_type: str
    excerpt: str
    confidence_score: int


@router.post("/generate", response_model=BRDResponse)
async def generate_brd(
    request: GenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate a new BRD for a project"""
    try:
        orchestrator = BRDOrchestrator(db)
        brd = await orchestrator.generate_brd(request.project_id)
        
        return BRDResponse(
            id=brd.id,
            project_id=brd.project_id,
            version=brd.version,
            title=brd.title,
            executive_summary=brd.executive_summary,
            full_document=brd.full_document,
            created_at=brd.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate BRD: {str(e)}")


@router.get("/{brd_id}", response_model=BRDResponse)
async def get_brd(
    brd_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get BRD details"""
    brd = await db.get(BRD, brd_id)
    if not brd:
        raise HTTPException(status_code=404, detail="BRD not found")
    
    return BRDResponse(
        id=brd.id,
        project_id=brd.project_id,
        version=brd.version,
        title=brd.title,
        executive_summary=brd.executive_summary,
        full_document=brd.full_document,
        created_at=brd.created_at.isoformat()
    )


@router.get("/{brd_id}/download")
async def download_brd(
    brd_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Download BRD as markdown file"""
    brd = await db.get(BRD, brd_id)
    if not brd:
        raise HTTPException(status_code=404, detail="BRD not found")
    
    return Response(
        content=brd.full_document,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f"attachment; filename={brd.title}.md"
        }
    )


@router.put("/{brd_id}/edit", response_model=BRDResponse)
async def edit_brd(
    brd_id: str,
    request: EditRequest,
    db: AsyncSession = Depends(get_db)
):
    """Edit BRD with natural language request"""
    editor = BRDEditor(db)
    
    try:
        brd = await editor.edit_brd(
            brd_id,
            request.edit_request,
            request.section
        )
        
        return BRDResponse(
            id=brd.id,
            project_id=brd.project_id,
            version=brd.version,
            title=brd.title,
            executive_summary=brd.executive_summary,
            full_document=brd.full_document,
            created_at=brd.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{brd_id}/history")
async def get_edit_history(
    brd_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get edit history for a BRD"""
    editor = BRDEditor(db)
    history = await editor.get_edit_history(brd_id)
    
    return {"brd_id": brd_id, "edit_history": history}


@router.get("/{brd_id}/citations", response_model=List[CitationResponse])
async def get_citations(
    brd_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all citations for a BRD"""
    brd = await db.get(BRD, brd_id)
    if not brd:
        raise HTTPException(status_code=404, detail="BRD not found")
    
    # Get all requirements for this project
    result = await db.execute(
        select(Requirement).where(Requirement.project_id == brd.project_id)
    )
    requirements = result.scalars().all()
    
    # Get citations for each requirement
    citations = []
    for req in requirements:
        for citation in req.citations:
            citations.append(CitationResponse(
                requirement_id=req.id,
                requirement_title=req.title,
                data_source_id=citation.data_source_id,
                source_type=citation.data_source.source_type.value,
                excerpt=citation.excerpt,
                confidence_score=citation.confidence_score
            ))
    
    return citations


@router.get("/project/{project_id}/brds", response_model=List[BRDResponse])
async def list_project_brds(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """List all BRDs for a project"""
    result = await db.execute(
        select(BRD)
        .where(BRD.project_id == project_id)
        .order_by(BRD.created_at.desc())
    )
    brds = result.scalars().all()
    
    return [
        BRDResponse(
            id=brd.id,
            project_id=brd.project_id,
            version=brd.version,
            title=brd.title,
            executive_summary=brd.executive_summary,
            full_document=brd.full_document,
            created_at=brd.created_at.isoformat()
        )
        for brd in brds
    ]
