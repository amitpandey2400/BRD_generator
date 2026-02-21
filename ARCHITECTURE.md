# System Architecture

## Overview

The BRD Generator is a comprehensive system that automatically generates Business Requirements Documents by ingesting data from multiple communication channels, filtering noise, extracting requirements, and producing structured, professional documentation.

## System Components

### 1. Data Ingestion Layer
**Purpose**: Collect data from multiple sources

**Components**:
- **Gmail Client** (`data_ingestion/gmail_client.py`)
  - Authenticates via OAuth 2.0
  - Fetches emails based on query filters
  - Extracts email threads and conversations
  - Returns structured message data

- **Slack Client** (`data_ingestion/slack_client.py`)
  - Connects via Slack API
  - Retrieves channel messages and threads
  - Searches across workspace
  - Enriches messages with user information

- **Fireflies Client** (`data_ingestion/fireflies_client.py`)
  - Fetches meeting transcripts via GraphQL
  - Extracts action items and keywords
  - Provides full transcript text
  - Includes speaker identification

- **Document Processor** (`data_ingestion/document_processor.py`)
  - Processes PDF, DOCX, PPTX, TXT, MD files
  - Extracts text content
  - Maintains document metadata
  - Handles file uploads

### 2. Processing Layer
**Purpose**: Analyze and extract structured information

**Components**:
- **Information Extractor** (`processing/extractor.py`)
  - Uses OpenAI GPT-4 for NLP tasks
  - Extracts:
    - Requirements (functional, non-functional)
    - Decisions and resolutions
    - Stakeholder information
    - Timelines and milestones
    - Assumptions and constraints
    - Success metrics and KPIs

- **Noise Filter** (`processing/noise_filter.py`)
  - Determines content relevance
  - Scores content by project relevance (0-100)
  - Categorizes content types
  - Extracts key points
  - Identifies duplicate content

- **Sentiment Analyzer** (`processing/sentiment_analyzer.py`)
  - Analyzes stakeholder sentiment
  - Extracts concerns and objections
  - Identifies positive feedback
  - Scores sentiment (-100 to +100)
  - Summarizes stakeholder positions

- **Conflict Detector** (`processing/conflict_detector.py`)
  - Identifies conflicting requirements
  - Detects incompatibilities
  - Assesses conflict severity
  - Suggests resolutions
  - Generates compatibility reports

### 3. BRD Generation Layer
**Purpose**: Generate and manage BRD documents

**Components**:
- **BRD Generator** (`brd_generator/generator.py`)
  - Generates document sections:
    - Executive Summary
    - Business Objectives
    - Stakeholder Analysis
    - Functional Requirements
    - Non-Functional Requirements
    - Assumptions & Constraints
    - Success Metrics
    - Timeline & Milestones
    - Risks & Mitigation
  - Compiles full document in Markdown
  - Maintains consistent formatting

- **BRD Editor** (`brd_generator/editor.py`)
  - Processes natural language edit requests
  - Identifies sections to modify
  - Applies edits intelligently
  - Maintains version history
  - Tracks all changes

- **BRD Orchestrator** (`brd_generator/orchestrator.py`)
  - Coordinates entire pipeline
  - Manages project lifecycle
  - Sequences operations
  - Handles error recovery
  - Updates project status

### 4. Storage Layer
**Purpose**: Persist and manage data

**Components**:
- **Database Models** (`storage/models.py`)
  - Project: Project metadata and status
  - DataSource: Ingested communications
  - Requirement: Extracted requirements
  - BRD: Generated documents
  - Citation: Requirement traceability
  - BRDEdit: Edit history
  - RequirementConflict: Detected conflicts
  - SentimentAnalysis: Stakeholder sentiment

- **Database Connection** (`storage/database.py`)
  - PostgreSQL with async support
  - Connection pooling
  - Session management
  - Schema migrations via Alembic

### 5. API Layer
**Purpose**: Expose functionality via REST API

**Components**:
- **Projects API** (`api/routes/projects.py`)
  - Create/list/get/delete projects
  - Trigger data ingestion
  - Process data
  - Generate BRDs

- **BRDs API** (`api/routes/brds.py`)
  - Retrieve BRDs
  - Download documents
  - Edit BRDs
  - View edit history
  - Get citations

- **Data Sources API** (`api/routes/data_sources.py`)
  - List data sources
  - View source details
  - Upload documents
  - Delete sources

- **Auth API** (`api/routes/auth.py`)
  - User authentication
  - Token management

### 6. Utility Layer
**Purpose**: Support functions

**Components**:
- **Logger** (`utils/logger.py`)
  - Structured logging
  - File and console output
  - Log level management

- **Traceability Matrix** (`utils/traceability.py`)
  - Generate requirement traceability
  - Map requirements to sources
  - Create markdown matrices
  - Track requirement lineage

## Data Flow

### Complete BRD Generation Flow

```
1. Project Creation
   └─> Create Project record
       └─> Status: CREATED

2. Data Ingestion
   ├─> Connect to Gmail API
   │   └─> Fetch relevant emails
   │       └─> Filter by query/date
   │           └─> Store as DataSource
   │
   ├─> Connect to Slack API
   │   └─> Fetch channel messages
   │       └─> Filter by relevance
   │           └─> Store as DataSource
   │
   ├─> Connect to Fireflies API
   │   └─> Fetch transcripts
   │       └─> Extract text
   │           └─> Store as DataSource
   │
   └─> Process Documents
       └─> Extract text from files
           └─> Store as DataSource
   
   Status: INGESTING → PROCESSING

3. Noise Filtering
   └─> For each DataSource
       ├─> Calculate relevance score
       ├─> Categorize content type
       └─> Mark as relevant/irrelevant

4. Information Extraction
   └─> For each relevant DataSource
       ├─> Extract requirements
       │   └─> Create Requirement records
       │       └─> Create Citations linking to source
       │
       ├─> Extract stakeholders
       ├─> Extract decisions
       ├─> Extract timeline items
       └─> Extract success metrics

5. Analysis
   ├─> Sentiment Analysis
   │   └─> Analyze stakeholder communications
   │       └─> Store sentiment data
   │
   └─> Conflict Detection
       └─> Compare requirements
           └─> Identify conflicts
               └─> Store conflicts

   Status: PROCESSING → READY

6. BRD Generation
   ├─> Generate Executive Summary
   ├─> Generate Business Objectives
   ├─> Generate Stakeholder Analysis
   ├─> Generate Functional Requirements
   ├─> Generate Non-Functional Requirements
   ├─> Generate Assumptions & Constraints
   ├─> Generate Success Metrics
   ├─> Generate Timeline
   └─> Compile Full Document
       └─> Store as BRD record

   Status: GENERATING → COMPLETED

7. Editing (Optional)
   └─> Receive edit request
       ├─> Identify section to edit
       ├─> Apply edit via AI
       ├─> Store in edit history
       ├─> Increment version
       └─> Update BRD
```

## Technology Stack

### Backend
- **Python 3.11+**: Core language
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **Alembic**: Database migrations
- **PostgreSQL**: Primary database
- **Redis**: Caching and task queue
- **Celery**: Async task processing

### AI/NLP
- **OpenAI GPT-4**: Text generation and analysis
- **LangChain**: AI application framework
- **spaCy**: NLP processing (optional)
- **Transformers**: ML models (optional)

### APIs
- **Gmail API**: Email integration
- **Slack SDK**: Slack integration
- **Fireflies GraphQL**: Meeting transcripts
- **Google OAuth 2.0**: Authentication

### Document Processing
- **python-docx**: Word documents
- **PyPDF2**: PDF files
- **python-pptx**: PowerPoint files
- **Markdown**: Output format

## Scalability Considerations

### Horizontal Scaling
- **API Servers**: Multiple FastAPI instances behind load balancer
- **Workers**: Multiple Celery workers for parallel processing
- **Database**: PostgreSQL replication and read replicas

### Vertical Scaling
- **Connection Pooling**: Efficient database connections
- **Caching**: Redis for frequently accessed data
- **Async Processing**: Non-blocking I/O operations

### Performance Optimization
- **Batch Processing**: Process multiple items together
- **Lazy Loading**: Load data only when needed
- **Query Optimization**: Indexed database queries
- **API Rate Limiting**: Prevent abuse

## Security

### Authentication & Authorization
- JWT tokens for API access
- OAuth 2.0 for external services
- Role-based access control (future)

### Data Protection
- Encrypted API credentials
- Secure credential storage
- HTTPS for all communications
- SQL injection prevention via ORM

### Privacy
- User data isolation
- Audit logging
- Data retention policies
- GDPR compliance considerations

## Monitoring & Observability

### Logging
- Structured JSON logs
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)
- File and console output
- Log rotation

### Metrics (Future)
- API response times
- Task completion rates
- Error rates
- Resource utilization

### Health Checks
- `/health` endpoint
- Database connectivity
- External API availability

## Deployment

### Local Development
```bash
python main.py
celery -A celery_tasks worker -l info
```

### Production (Recommended)
- **Container**: Docker/Kubernetes
- **Process Manager**: systemd or supervisor
- **Web Server**: Nginx reverse proxy
- **ASGI Server**: Uvicorn with Gunicorn
- **Database**: Managed PostgreSQL (AWS RDS, etc.)
- **Cache**: Managed Redis (AWS ElastiCache, etc.)

## Extension Points

### Adding New Data Sources
1. Create new client in `data_ingestion/`
2. Implement standard interface
3. Add to orchestrator
4. Update data source types enum

### Custom Processing
1. Add processor in `processing/`
2. Integrate with orchestrator
3. Update database models if needed

### New BRD Sections
1. Add generator method in `brd_generator/generator.py`
2. Update database model
3. Update compilation method

### Additional APIs
1. Create route file in `api/routes/`
2. Define Pydantic models
3. Register in main.py
