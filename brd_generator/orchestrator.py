"""
BRD Orchestrator - Coordinates the entire BRD generation process
"""
from typing import Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from storage.models import (
    Project, DataSource, Requirement, BRD, Citation,
    ProjectStatus, DataSourceType, RequirementType
)
from data_ingestion.gmail_client import GmailClient
from data_ingestion.slack_client import SlackClient
from data_ingestion.fireflies_client import FirefliesClient
from data_ingestion.document_processor import DocumentProcessor
from processing.extractor import InformationExtractor
from processing.noise_filter import NoiseFilter
from processing.sentiment_analyzer import SentimentAnalyzer
from processing.conflict_detector import ConflictDetector
from brd_generator.generator import BRDGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


class BRDOrchestrator:
    """Main orchestrator for BRD generation pipeline"""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.gmail = None
        self.slack = None
        self.fireflies = None
        self.doc_processor = DocumentProcessor()
        self.extractor = InformationExtractor()
        self.noise_filter = NoiseFilter()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.conflict_detector = ConflictDetector()
        self.brd_generator = BRDGenerator()
    
    async def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project"""
        project = Project(
            name=name,
            description=description,
            status=ProjectStatus.CREATED
        )
        
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        
        logger.info(f"Created project: {project.id} - {name}")
        return project
    
    async def ingest_data(
        self,
        project_id: str,
        sources: Dict[str, any]
    ) -> Dict:
        """
        Ingest data from multiple sources
        
        Args:
            project_id: Project ID
            sources: Dictionary with source configurations
                {
                    'gmail': {'query': '...', 'days_back': 30},
                    'slack': {'channels': [...], 'days_back': 30},
                    'fireflies': {'days_back': 30},
                    'documents': [file_paths]
                }
        """
        # Update project status
        project = await self.db.get(Project, project_id)
        project.status = ProjectStatus.INGESTING
        await self.db.commit()
        
        ingested_count = 0
        
        try:
            # Gmail
            if 'gmail' in sources and sources['gmail']:
                count = await self._ingest_gmail(project_id, sources['gmail'])
                ingested_count += count
            
            # Slack
            if 'slack' in sources and sources['slack']:
                count = await self._ingest_slack(project_id, sources['slack'])
                ingested_count += count
            
            # Fireflies
            if 'fireflies' in sources and sources['fireflies']:
                count = await self._ingest_fireflies(project_id, sources['fireflies'])
                ingested_count += count
            
            # Documents
            if 'documents' in sources and sources['documents']:
                count = await self._ingest_documents(project_id, sources['documents'])
                ingested_count += count
            
            # Update project status
            project.status = ProjectStatus.PROCESSING
            await self.db.commit()
            
            logger.info(f"Ingested {ingested_count} data sources for project {project_id}")
            
            return {
                'project_id': project_id,
                'ingested_count': ingested_count,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error ingesting data: {e}")
            project.status = ProjectStatus.ERROR
            await self.db.commit()
            raise
    
    async def _ingest_gmail(self, project_id: str, config: Dict) -> int:
        """Ingest Gmail messages"""
        if not self.gmail:
            self.gmail = GmailClient()
            self.gmail.authenticate()
        
        messages = self.gmail.get_messages(
            query=config.get('query'),
            days_back=config.get('days_back', 30)
        )
        
        for msg in messages:
            # Filter noise
            relevance = await self.noise_filter.is_relevant(
                msg['body'],
                project_context=config.get('context')
            )
            
            if relevance['is_relevant']:
                data_source = DataSource(
                    project_id=project_id,
                    source_type=DataSourceType.EMAIL,
                    source_identifier=msg['id'],
                    raw_content=msg['body'],
                    metadata_json={
                        'subject': msg['subject'],
                        'from': msg['from'],
                        'date': msg['date']
                    },
                    relevance_score=relevance['relevance_score']
                )
                self.db.add(data_source)
        
        await self.db.commit()
        return len(messages)
    
    async def _ingest_slack(self, project_id: str, config: Dict) -> int:
        """Ingest Slack messages"""
        if not self.slack:
            self.slack = SlackClient()
        
        all_messages = []
        
        for channel_id in config.get('channels', []):
            messages = self.slack.get_channel_messages(
                channel_id,
                days_back=config.get('days_back', 30)
            )
            all_messages.extend(messages)
        
        for msg in all_messages:
            text = msg.get('text', '')
            if text:
                relevance = await self.noise_filter.is_relevant(text)
                
                if relevance['is_relevant']:
                    data_source = DataSource(
                        project_id=project_id,
                        source_type=DataSourceType.SLACK,
                        source_identifier=msg.get('ts'),
                        raw_content=text,
                        metadata_json={
                            'user': msg.get('user_name'),
                            'channel': msg.get('channel'),
                            'timestamp': msg.get('ts')
                        },
                        relevance_score=relevance['relevance_score']
                    )
                    self.db.add(data_source)
        
        await self.db.commit()
        return len(all_messages)
    
    async def _ingest_fireflies(self, project_id: str, config: Dict) -> int:
        """Ingest Fireflies meeting transcripts"""
        if not self.fireflies:
            self.fireflies = FirefliesClient()
        
        transcripts = self.fireflies.get_transcripts(
            days_back=config.get('days_back', 30)
        )
        
        for transcript in transcripts:
            text = self.fireflies.get_transcript_text(transcript['id'])
            
            if text:
                data_source = DataSource(
                    project_id=project_id,
                    source_type=DataSourceType.MEETING,
                    source_identifier=transcript['id'],
                    raw_content=text,
                    metadata_json={
                        'title': transcript.get('title'),
                        'date': transcript.get('date'),
                        'participants': transcript.get('participants'),
                        'summary': transcript.get('summary')
                    },
                    relevance_score=100  # Meetings are generally relevant
                )
                self.db.add(data_source)
        
        await self.db.commit()
        return len(transcripts)
    
    async def _ingest_documents(self, project_id: str, file_paths: List[str]) -> int:
        """Ingest uploaded documents"""
        for file_path in file_paths:
            try:
                doc_data = self.doc_processor.process_file(file_path)
                
                data_source = DataSource(
                    project_id=project_id,
                    source_type=DataSourceType.DOCUMENT,
                    source_identifier=file_path,
                    raw_content=doc_data['content'],
                    metadata_json=doc_data['metadata'],
                    relevance_score=100  # Uploaded docs are intentionally relevant
                )
                self.db.add(data_source)
                
            except Exception as e:
                logger.error(f"Error processing document {file_path}: {e}")
        
        await self.db.commit()
        return len(file_paths)
    
    async def process_and_extract(self, project_id: str) -> Dict:
        """Process ingested data and extract requirements"""
        # Get all data sources
        result = await self.db.execute(
            select(DataSource).where(DataSource.project_id == project_id)
        )
        data_sources = result.scalars().all()
        
        all_requirements = []
        
        for ds in data_sources:
            # Extract requirements
            requirements = await self.extractor.extract_requirements(ds.raw_content)
            
            for req in requirements:
                requirement = Requirement(
                    project_id=project_id,
                    requirement_type=RequirementType(req['type']),
                    title=req['title'],
                    description=req['description'],
                    priority=req.get('priority', 'Medium'),
                    stakeholder=req.get('stakeholder'),
                    acceptance_criteria=req.get('acceptance_criteria')
                )
                self.db.add(requirement)
                await self.db.flush()
                
                # Create citation
                citation = Citation(
                    requirement_id=requirement.id,
                    data_source_id=ds.id,
                    excerpt=req['description'][:500]
                )
                self.db.add(citation)
                
                all_requirements.append(req)
        
        await self.db.commit()
        
        logger.info(f"Extracted {len(all_requirements)} requirements for project {project_id}")
        
        return {
            'project_id': project_id,
            'requirements_count': len(all_requirements),
            'status': 'success'
        }
    
    async def generate_brd(self, project_id: str) -> BRD:
        """Generate complete BRD for a project"""
        # Update status
        project = await self.db.get(Project, project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
            
        project.status = ProjectStatus.GENERATING
        await self.db.commit()
        
        logger.info(f"Starting BRD generation for project: {project.name}")
        
        # Get all requirements
        result = await self.db.execute(
            select(Requirement).where(Requirement.project_id == project_id)
        )
        requirements = result.scalars().all()
        
        logger.info(f"Found {len(requirements)} requirements for project")
        
        # Convert to dicts
        req_dicts = [
            {
                'type': req.requirement_type.value,
                'title': req.title,
                'description': req.description,
                'priority': req.priority,
                'stakeholder': req.stakeholder
            }
            for req in requirements
        ]
        
        # If no requirements, create basic ones from project description
        if not req_dicts and project.description:
            logger.info("No requirements found, using project description")
            req_dicts = [
                {
                    'type': 'functional',
                    'title': 'Project Implementation',
                    'description': project.description,
                    'priority': 'high',
                    'stakeholder': 'Project Team'
                }
            ]
        
        # Generate sections
        sections = {}
        
        sections['executive_summary'] = await self.brd_generator.generate_executive_summary(
            project.name,
            req_dicts,
            [],  # Stakeholders would be extracted
            []   # Objectives would be extracted
        )
        
        sections['functional_requirements'] = await self.brd_generator.generate_functional_requirements(
            req_dicts
        )
        
        sections['non_functional_requirements'] = await self.brd_generator.generate_non_functional_requirements(
            req_dicts
        )
        
        # Generate full document
        full_doc = await self.brd_generator.generate_full_document(
            project.name,
            sections
        )
        
        # Save BRD
        brd = BRD(
            project_id=project_id,
            title=f"{project.name} - Business Requirements Document",
            executive_summary=sections.get('executive_summary'),
            functional_requirements=sections.get('functional_requirements'),
            non_functional_requirements=sections.get('non_functional_requirements'),
            full_document=full_doc
        )
        
        self.db.add(brd)
        project.status = ProjectStatus.COMPLETED
        await self.db.commit()
        await self.db.refresh(brd)
        
        logger.info(f"Generated BRD {brd.id} for project {project_id}")
        
        return brd
