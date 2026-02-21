# Project Structure

```
Bussines manager/
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── alembic.ini                  # Alembic configuration
├── celery_tasks.py              # Celery async tasks
│
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
├── ARCHITECTURE.md              # System architecture
├── LICENSE                      # MIT License
│
├── config/                      # Configuration
│   ├── __init__.py
│   └── settings.py              # Application settings
│
├── storage/                     # Data persistence
│   ├── __init__.py
│   ├── database.py              # Database connection
│   ├── models.py                # SQLAlchemy models
│   ├── documents/               # Uploaded documents
│   │   └── .gitkeep
│   └── temp/                    # Temporary files
│       └── .gitkeep
│
├── data_ingestion/              # Data source integrations
│   ├── __init__.py
│   ├── gmail_client.py          # Gmail API client
│   ├── slack_client.py          # Slack API client
│   ├── fireflies_client.py      # Fireflies API client
│   └── document_processor.py    # Document file processor
│
├── processing/                  # NLP and analysis
│   ├── __init__.py
│   ├── extractor.py             # Information extraction
│   ├── noise_filter.py          # Relevance filtering
│   ├── sentiment_analyzer.py    # Sentiment analysis
│   └── conflict_detector.py     # Conflict detection
│
├── brd_generator/               # BRD generation
│   ├── __init__.py
│   ├── generator.py             # Document generation
│   ├── editor.py                # Natural language editing
│   └── orchestrator.py          # Pipeline orchestration
│
├── api/                         # REST API
│   ├── __init__.py
│   └── routes/
│       ├── auth.py              # Authentication
│       ├── projects.py          # Project endpoints
│       ├── brds.py              # BRD endpoints
│       └── data_sources.py      # Data source endpoints
│
├── utils/                       # Utilities
│   ├── __init__.py
│   ├── logger.py                # Logging setup
│   └── traceability.py          # Traceability matrix
│
├── alembic/                     # Database migrations
│   └── env.py                   # Migration environment
│
├── logs/                        # Application logs
│   └── .gitkeep
│
├── tests/                       # Test suite
│   ├── test_extraction.py       # Extraction tests
│   └── test_filtering.py        # Filtering tests
│
└── examples/                    # Usage examples
    └── basic_usage.py           # Basic usage example
```

## Module Descriptions

### Core Modules

**main.py**
- FastAPI application setup
- Route registration
- CORS configuration
- Lifespan events

**config/settings.py**
- Environment configuration
- API keys management
- Database settings
- Feature flags

### Data Ingestion

**data_ingestion/gmail_client.py**
- Gmail OAuth authentication
- Email fetching with filters
- Thread retrieval
- Message parsing

**data_ingestion/slack_client.py**
- Slack API integration
- Channel message retrieval
- Thread replies
- User enrichment

**data_ingestion/fireflies_client.py**
- Meeting transcript fetching
- Action item extraction
- Speaker identification
- Transcript search

**data_ingestion/document_processor.py**
- PDF text extraction
- DOCX processing
- PPTX slide parsing
- File upload handling

### Processing & Analysis

**processing/extractor.py**
- Requirement extraction
- Decision identification
- Stakeholder extraction
- Timeline parsing
- Success metrics extraction

**processing/noise_filter.py**
- Relevance scoring (0-100)
- Content categorization
- Key point extraction
- Deduplication

**processing/sentiment_analyzer.py**
- Sentiment analysis (-100 to +100)
- Concern extraction
- Stakeholder feedback summary
- Emotion detection

**processing/conflict_detector.py**
- Requirement conflict detection
- Compatibility checking
- Conflict resolution suggestions
- Severity assessment

### BRD Generation

**brd_generator/generator.py**
- Section generation (AI-powered)
- Document compilation
- Markdown formatting
- Template management

**brd_generator/editor.py**
- Natural language editing
- Section identification
- Version management
- Edit history tracking

**brd_generator/orchestrator.py**
- Pipeline coordination
- Status management
- Error handling
- Multi-source ingestion

### Storage

**storage/models.py**
- Project model
- DataSource model
- Requirement model
- BRD model
- Citation model
- Conflict model
- Sentiment model
- Edit history model

**storage/database.py**
- Async database engine
- Session management
- Connection pooling
- Schema initialization

### API

**api/routes/projects.py**
- POST /api/projects - Create project
- GET /api/projects - List projects
- POST /api/projects/{id}/ingest - Ingest data
- POST /api/projects/{id}/generate-brd - Generate BRD

**api/routes/brds.py**
- GET /api/brds/{id} - Get BRD
- GET /api/brds/{id}/download - Download BRD
- PUT /api/brds/{id}/edit - Edit BRD
- GET /api/brds/{id}/citations - Get citations

**api/routes/data_sources.py**
- GET /api/data-sources/project/{id}/sources - List sources
- POST /api/data-sources/upload - Upload document
- DELETE /api/data-sources/{id} - Delete source

### Utilities

**utils/logger.py**
- Structured logging
- File and console handlers
- Log rotation
- Level management

**utils/traceability.py**
- Requirement traceability matrix
- Source-to-requirement mapping
- Markdown matrix generation
- Citation tracking

### Testing

**tests/test_extraction.py**
- Requirement extraction tests
- Decision extraction tests
- Stakeholder identification tests

**tests/test_filtering.py**
- Relevance detection tests
- Content categorization tests
- Key point extraction tests

### Background Tasks

**celery_tasks.py**
- Async project processing
- Background data ingestion
- Scheduled tasks
- Task monitoring

## Key Features by Module

### 1. Multi-Source Data Ingestion
- Email (Gmail API)
- Chat (Slack API)
- Meetings (Fireflies API)
- Documents (PDF, DOCX, PPTX)

### 2. Intelligent Processing
- AI-powered extraction (GPT-4)
- Noise filtering
- Sentiment analysis
- Conflict detection

### 3. BRD Generation
- Structured document creation
- Professional formatting
- Citation tracking
- Version management

### 4. Editing & Collaboration
- Natural language editing
- Section-specific updates
- Change history
- Version control

### 5. API & Integration
- RESTful API
- Async processing
- File uploads
- Export capabilities

## Database Schema

**Projects**
- id, name, description, status, timestamps

**DataSources**
- id, project_id, source_type, content, metadata, relevance_score

**Requirements**
- id, project_id, type, title, description, priority, stakeholder

**BRDs**
- id, project_id, version, sections (9 main sections), full_document

**Citations**
- id, requirement_id, data_source_id, excerpt, confidence

**Conflicts**
- id, req1_id, req2_id, description, severity, resolution

**BRDEdits**
- id, brd_id, edit_request, section, previous_content, new_content

**SentimentAnalysis**
- id, data_source_id, stakeholder, sentiment, score, concerns

## Configuration Files

**.env**
- API keys (OpenAI, Gmail, Slack, Fireflies)
- Database connection
- Redis URL
- Feature flags

**alembic.ini**
- Database migration settings
- Logging configuration

**requirements.txt**
- Python package dependencies
- Pinned versions

## Deployment Structure

```
Production/
├── Docker Container
│   ├── Application (main.py)
│   ├── Celery Worker
│   └── Dependencies
│
├── PostgreSQL Database
│   ├── Application data
│   └── Vector embeddings (future)
│
├── Redis Cache
│   ├── Session storage
│   └── Task queue
│
└── Storage
    ├── Uploaded documents
    └── Generated BRDs
```

## Development Workflow

1. **Setup**: Install dependencies, configure .env
2. **Database**: Run migrations with Alembic
3. **Development**: Run main.py with --reload
4. **Testing**: Run pytest test suite
5. **Background Tasks**: Start Celery worker
6. **API Testing**: Use /docs for Swagger UI

## Future Enhancements

- [ ] Frontend dashboard (React)
- [ ] Real-time WebSocket updates
- [ ] PDF/Word export
- [ ] User authentication & authorization
- [ ] Multi-tenant support
- [ ] Advanced analytics dashboard
- [ ] Requirement dependency graphs
- [ ] Automated testing coverage
- [ ] CI/CD pipeline
- [ ] Docker containerization
