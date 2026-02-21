"""
API routes for data sources
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List
from sqlalchemy import select

from storage.database import get_db
from storage.models import DataSource
from data_ingestion.document_processor import DocumentProcessor
from config.settings import settings

router = APIRouter()


class DataSourceResponse(BaseModel):
    id: str
    project_id: str
    source_type: str
    source_identifier: str
    relevance_score: int
    is_relevant: bool
    created_at: str
    
    class Config:
        from_attributes = True


@router.get("/project/{project_id}/sources", response_model=List[DataSourceResponse])
async def list_data_sources(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """List all data sources for a project"""
    result = await db.execute(
        select(DataSource)
        .where(DataSource.project_id == project_id)
        .order_by(DataSource.created_at.desc())
    )
    sources = result.scalars().all()
    
    return [
        DataSourceResponse(
            id=src.id,
            project_id=src.project_id,
            source_type=src.source_type.value,
            source_identifier=src.source_identifier,
            relevance_score=src.relevance_score,
            is_relevant=src.is_relevant,
            created_at=src.created_at.isoformat()
        )
        for src in sources
    ]


@router.get("/{source_id}")
async def get_data_source(
    source_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get data source details"""
    source = await db.get(DataSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    return {
        "id": source.id,
        "project_id": source.project_id,
        "source_type": source.source_type.value,
        "source_identifier": source.source_identifier,
        "raw_content": source.raw_content,
        "processed_content": source.processed_content,
        "metadata": source.metadata_json,
        "relevance_score": source.relevance_score,
        "is_relevant": source.is_relevant,
        "created_at": source.created_at.isoformat()
    }


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    project_id: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload a document for processing"""
    import traceback
    from brd_generator.orchestrator import BRDOrchestrator
    from storage.models import Project, DataSourceType, DataSource
    
    try:
        # Validate project_id
        if not project_id:
            raise HTTPException(status_code=400, detail="project_id is required")
            
        # Check project exists
        project = await db.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Check file size
        contents = await file.read()
        if len(contents) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Save file
        doc_processor = DocumentProcessor()
        file_path = doc_processor.save_uploaded_file(contents, file.filename)
        
        # Process document to extract text
        doc_data = doc_processor.process_file(file_path)
        
        # Save as DataSource in database
        data_source = DataSource(
            project_id=project_id,
            source_type=DataSourceType.DOCUMENT,
            source_identifier=file_path,
            raw_content=doc_data['content'],
            metadata_json=doc_data['metadata'],
            relevance_score=100,  # Uploaded docs are intentionally relevant
            is_relevant=True
        )
        db.add(data_source)
        await db.commit()
        await db.refresh(data_source)
        
        # Extract requirements from document
        orchestrator = BRDOrchestrator(db)
        await orchestrator.process_and_extract(project_id)
        
        return {
            "filename": file.filename,
            "file_path": file_path,
            "size": len(contents),
            "data_source_id": data_source.id,
            "message": "File uploaded and processed successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error uploading document: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.delete("/{source_id}")
async def delete_data_source(
    source_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a data source"""
    source = await db.get(DataSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    await db.delete(source)
    await db.commit()
    
    return {"message": "Data source deleted successfully"}
