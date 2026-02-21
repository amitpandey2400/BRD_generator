"""
Database models for BRD Generator
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
import uuid

from storage.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class ProjectStatus(str, Enum):
    """Project status enumeration"""
    CREATED = "created"
    INGESTING = "ingesting"
    PROCESSING = "processing"
    READY = "ready"
    GENERATING = "generating"
    COMPLETED = "completed"
    ERROR = "error"


class DataSourceType(str, Enum):
    """Data source types"""
    EMAIL = "email"
    SLACK = "slack"
    MEETING = "meeting"
    DOCUMENT = "document"
    MANUAL = "manual"


class RequirementType(str, Enum):
    """Requirement types"""
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS = "business"
    TECHNICAL = "technical"
    CONSTRAINT = "constraint"


class Project(Base):
    """Project model"""
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.CREATED)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    data_sources = relationship("DataSource", back_populates="project", cascade="all, delete-orphan")
    requirements = relationship("Requirement", back_populates="project", cascade="all, delete-orphan")
    brds = relationship("BRD", back_populates="project", cascade="all, delete-orphan")
    metadata_json = Column(JSON, default=dict)


class DataSource(Base):
    """Data source model for tracking ingested data"""
    __tablename__ = "data_sources"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"))
    source_type = Column(SQLEnum(DataSourceType), nullable=False)
    source_identifier = Column(String(500))  # Email ID, Slack channel, etc.
    raw_content = Column(Text)
    processed_content = Column(Text)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    is_relevant = Column(Boolean, default=True)
    relevance_score = Column(Integer, default=0)
    
    # Relationships
    project = relationship("Project", back_populates="data_sources")
    citations = relationship("Citation", back_populates="data_source")


class Requirement(Base):
    """Extracted requirement model"""
    __tablename__ = "requirements"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"))
    requirement_type = Column(SQLEnum(RequirementType), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(50))  # High, Medium, Low
    stakeholder = Column(String(255))
    acceptance_criteria = Column(Text)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="requirements")
    citations = relationship("Citation", back_populates="requirement")
    conflicts = relationship("RequirementConflict", foreign_keys="[RequirementConflict.requirement_id]")


class BRD(Base):
    """Business Requirements Document model"""
    __tablename__ = "brds"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"))
    version = Column(Integer, default=1)
    title = Column(String(500), nullable=False)
    
    # BRD Sections
    executive_summary = Column(Text)
    business_objectives = Column(Text)
    stakeholder_analysis = Column(Text)
    functional_requirements = Column(Text)
    non_functional_requirements = Column(Text)
    assumptions = Column(Text)
    constraints = Column(Text)
    success_metrics = Column(Text)
    timeline = Column(Text)
    risks = Column(Text)
    
    # Metadata
    full_document = Column(Text)  # Complete formatted document
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="brds")
    edit_history = relationship("BRDEdit", back_populates="brd", cascade="all, delete-orphan")


class BRDEdit(Base):
    """BRD edit history"""
    __tablename__ = "brd_edits"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    brd_id = Column(String, ForeignKey("brds.id"))
    edit_request = Column(Text, nullable=False)
    section_affected = Column(String(255))
    previous_content = Column(Text)
    new_content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    brd = relationship("BRD", back_populates="edit_history")


class Citation(Base):
    """Citation linking requirements to data sources"""
    __tablename__ = "citations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    requirement_id = Column(String, ForeignKey("requirements.id"))
    data_source_id = Column(String, ForeignKey("data_sources.id"))
    excerpt = Column(Text)  # The specific excerpt from the source
    confidence_score = Column(Integer, default=100)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    requirement = relationship("Requirement", back_populates="citations")
    data_source = relationship("DataSource", back_populates="citations")


class RequirementConflict(Base):
    """Detected conflicts between requirements"""
    __tablename__ = "requirement_conflicts"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    requirement_id = Column(String, ForeignKey("requirements.id"))
    conflicting_requirement_id = Column(String, ForeignKey("requirements.id"))
    conflict_description = Column(Text)
    severity = Column(String(50))  # High, Medium, Low
    resolution_status = Column(String(50), default="unresolved")
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    requirement = relationship("Requirement", foreign_keys=[requirement_id])
    conflicting_requirement = relationship("Requirement", foreign_keys=[conflicting_requirement_id])


class SentimentAnalysis(Base):
    """Sentiment analysis for stakeholder communications"""
    __tablename__ = "sentiment_analysis"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    data_source_id = Column(String, ForeignKey("data_sources.id"))
    stakeholder = Column(String(255))
    sentiment = Column(String(50))  # positive, negative, neutral
    sentiment_score = Column(Integer)  # -100 to 100
    concerns = Column(JSON, default=list)  # List of extracted concerns
    created_at = Column(DateTime, default=func.now())
