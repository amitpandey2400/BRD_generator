"""
Example script for using the BRD Generator
"""
import asyncio
from storage.database import AsyncSessionLocal
from brd_generator.orchestrator import BRDOrchestrator


async def main():
    """Example usage of BRD Generator"""
    
    # Create database session
    async with AsyncSessionLocal() as db:
        # Initialize orchestrator
        orchestrator = BRDOrchestrator(db)
        
        # 1. Create a new project
        print("Creating project...")
        project = await orchestrator.create_project(
            name="E-Commerce Platform Redesign",
            description="Redesign of the company's e-commerce platform to improve user experience and increase conversion rates"
        )
        print(f"Project created: {project.id}")
        
        # 2. Ingest data from various sources
        print("\nIngesting data...")
        sources = {
            'gmail': {
                'query': 'subject:ecommerce OR subject:platform redesign',
                'days_back': 60,
                'context': 'E-commerce platform redesign project'
            },
            'slack': {
                'channels': ['C01234567', 'C01234568'],  # Replace with actual channel IDs
                'days_back': 60
            },
            'fireflies': {
                'days_back': 60
            },
            'documents': [
                './storage/documents/requirements_draft.docx',
                './storage/documents/stakeholder_feedback.pdf'
            ]
        }
        
        # Note: Uncomment to actually ingest data
        # ingestion_result = await orchestrator.ingest_data(project.id, sources)
        # print(f"Ingested {ingestion_result['ingested_count']} data sources")
        
        # 3. Process data and extract requirements
        print("\nProcessing data and extracting requirements...")
        # process_result = await orchestrator.process_and_extract(project.id)
        # print(f"Extracted {process_result['requirements_count']} requirements")
        
        # 4. Generate BRD
        print("\nGenerating BRD...")
        # brd = await orchestrator.generate_brd(project.id)
        # print(f"BRD generated: {brd.id}")
        # print(f"\nPreview:\n{brd.executive_summary[:500]}...")
        
        print("\n✓ Example completed!")
        print(f"\nTo view the BRD, visit: http://localhost:8000/api/brds/{project.id}")


if __name__ == "__main__":
    asyncio.run(main())
