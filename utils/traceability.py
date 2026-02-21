"""
Requirement Traceability Matrix Generator
"""
from typing import List, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from storage.models import Requirement, Citation, DataSource
from utils.logger import get_logger

logger = get_logger(__name__)


class TraceabilityMatrix:
    """Generate requirement traceability matrices"""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def generate_matrix(self, project_id: str) -> Dict:
        """
        Generate traceability matrix for a project
        
        Returns:
            Dictionary with matrix data
        """
        # Get all requirements
        result = await self.db.execute(
            select(Requirement).where(Requirement.project_id == project_id)
        )
        requirements = result.scalars().all()
        
        matrix_data = []
        
        for req in requirements:
            # Get citations (sources)
            sources = []
            for citation in req.citations:
                source = citation.data_source
                sources.append({
                    'source_type': source.source_type.value,
                    'source_id': source.source_identifier,
                    'excerpt': citation.excerpt[:100] + '...' if len(citation.excerpt) > 100 else citation.excerpt,
                    'confidence': citation.confidence_score
                })
            
            matrix_data.append({
                'requirement_id': req.id,
                'requirement_type': req.requirement_type.value,
                'title': req.title,
                'priority': req.priority,
                'stakeholder': req.stakeholder,
                'sources': sources,
                'source_count': len(sources)
            })
        
        logger.info(f"Generated traceability matrix with {len(matrix_data)} requirements")
        
        return {
            'project_id': project_id,
            'total_requirements': len(matrix_data),
            'matrix': matrix_data
        }
    
    async def generate_markdown_matrix(self, project_id: str) -> str:
        """Generate traceability matrix as markdown table"""
        matrix = await self.generate_matrix(project_id)
        
        markdown = "# Requirement Traceability Matrix\n\n"
        markdown += f"**Project ID:** {project_id}\n\n"
        markdown += f"**Total Requirements:** {matrix['total_requirements']}\n\n"
        
        # Create table
        markdown += "| Req ID | Type | Title | Priority | Sources | Stakeholder |\n"
        markdown += "|--------|------|-------|----------|---------|-------------|\n"
        
        for row in matrix['matrix']:
            req_id_short = row['requirement_id'][:8]
            sources = f"{row['source_count']} sources"
            markdown += f"| {req_id_short} | {row['requirement_type']} | {row['title'][:30]} | {row['priority']} | {sources} | {row['stakeholder'] or 'N/A'} |\n"
        
        # Add detailed sources section
        markdown += "\n\n## Detailed Source Mapping\n\n"
        
        for row in matrix['matrix']:
            markdown += f"### {row['title']}\n\n"
            markdown += f"**ID:** {row['requirement_id']}\n\n"
            markdown += "**Sources:**\n\n"
            
            for source in row['sources']:
                markdown += f"- **{source['source_type']}** (ID: {source['source_id'][:20]}...)\n"
                markdown += f"  - Excerpt: \"{source['excerpt']}\"\n"
                markdown += f"  - Confidence: {source['confidence']}%\n\n"
        
        return markdown
    
    async def get_requirement_sources(self, requirement_id: str) -> List[Dict]:
        """Get all sources for a specific requirement"""
        requirement = await self.db.get(Requirement, requirement_id)
        if not requirement:
            return []
        
        sources = []
        for citation in requirement.citations:
            source = citation.data_source
            sources.append({
                'citation_id': citation.id,
                'source_id': source.id,
                'source_type': source.source_type.value,
                'source_identifier': source.source_identifier,
                'excerpt': citation.excerpt,
                'confidence_score': citation.confidence_score,
                'metadata': source.metadata_json
            })
        
        return sources
    
    async def find_requirements_by_source(self, source_id: str) -> List[Dict]:
        """Find all requirements linked to a specific source"""
        result = await self.db.execute(
            select(Citation).where(Citation.data_source_id == source_id)
        )
        citations = result.scalars().all()
        
        requirements = []
        for citation in citations:
            req = citation.requirement
            requirements.append({
                'requirement_id': req.id,
                'title': req.title,
                'type': req.requirement_type.value,
                'excerpt': citation.excerpt,
                'confidence': citation.confidence_score
            })
        
        return requirements
