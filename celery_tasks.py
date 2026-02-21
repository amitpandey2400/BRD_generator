"""
Celery task configuration for async processing
"""
from celery import Celery
from config.settings import settings

# Initialize Celery
celery_app = Celery(
    'brd_generator',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)


@celery_app.task(name='process_project')
def process_project_task(project_id: str):
    """
    Background task to process a project
    
    Args:
        project_id: Project ID to process
    """
    import asyncio
    from storage.database import AsyncSessionLocal
    from brd_generator.orchestrator import BRDOrchestrator
    
    async def process():
        async with AsyncSessionLocal() as db:
            orchestrator = BRDOrchestrator(db)
            
            # Process and extract
            result = await orchestrator.process_and_extract(project_id)
            
            # Generate BRD
            brd = await orchestrator.generate_brd(project_id)
            
            return {
                'project_id': project_id,
                'brd_id': brd.id,
                'requirements_count': result['requirements_count']
            }
    
    return asyncio.run(process())


@celery_app.task(name='ingest_data')
def ingest_data_task(project_id: str, sources: dict):
    """
    Background task to ingest data
    
    Args:
        project_id: Project ID
        sources: Source configurations
    """
    import asyncio
    from storage.database import AsyncSessionLocal
    from brd_generator.orchestrator import BRDOrchestrator
    
    async def ingest():
        async with AsyncSessionLocal() as db:
            orchestrator = BRDOrchestrator(db)
            result = await orchestrator.ingest_data(project_id, sources)
            return result
    
    return asyncio.run(ingest())


# Optional: Periodic tasks
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Set up periodic tasks"""
    # Example: Check for new emails every hour
    # sender.add_periodic_task(3600.0, check_new_emails.s(), name='check emails')
    pass
