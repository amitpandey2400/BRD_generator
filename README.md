---
title: BRD Generator
emoji: 📄
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# Business Requirements Document (BRD) Generator

An intelligent system that automatically generates comprehensive Business Requirements Documents by ingesting data from multiple communication channels.

## Features

- **Multi-Channel Data Ingestion**: Gmail, Slack, meeting transcripts (Fireflies), uploaded documents
- **Intelligent Filtering**: Extracts project-relevant information while filtering noise
- **Structured BRD Generation**: Creates professional documents with standard sections
- **Iterative Editing**: Natural language edit requests for document modifications
- **Citation & Traceability**: Links requirements to original sources
- **Conflict Detection**: Identifies conflicting requirements across sources
- **Sentiment Analysis**: Analyzes stakeholder concerns and feedback
- **Traceability Matrix**: Generates requirement traceability matrices

## Architecture

```
├── data_ingestion/       # Channel integrations (Gmail, Slack, etc.)
├── processing/           # NLP, filtering, extraction engines
├── brd_generator/        # Document generation and templates
├── storage/              # Database models and repositories
├── api/                  # REST API endpoints
├── web/                  # Frontend dashboard
├── utils/                # Common utilities
└── config/               # Configuration management
```

## Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **AI/NLP**: OpenAI GPT-4, LangChain, spaCy
- **Database**: PostgreSQL with pgvector for embeddings
- **Cache**: Redis
- **Frontend**: React with TypeScript
- **APIs**: Gmail API, Slack API, Fireflies API

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in `.env`
4. Run migrations: `alembic upgrade head`
5. Start the server: `uvicorn main:app --reload`

## Configuration

Create a `.env` file with:
```
OPENAI_API_KEY=your_key
GMAIL_CLIENT_ID=your_id
GMAIL_CLIENT_SECRET=your_secret
SLACK_BOT_TOKEN=your_token
SLACK_APP_TOKEN=your_app_token
FIREFLIES_API_KEY=your_key
DATABASE_URL=postgresql://user:pass@localhost/brd_db
REDIS_URL=redis://localhost:6379
```

## Usage

### Starting the System
```bash
python main.py
```

### Generating a BRD
```python
from brd_generator.orchestrator import BRDOrchestrator

orchestrator = BRDOrchestrator()
project_id = orchestrator.create_project("Project Alpha")
orchestrator.ingest_data(project_id)
brd = orchestrator.generate_brd(project_id)
```

### Editing a BRD
```python
orchestrator.edit_brd(brd_id, "Add a section about data privacy requirements")
```

## API Endpoints

- `POST /api/projects` - Create a new project
- `POST /api/projects/{id}/ingest` - Trigger data ingestion
- `POST /api/projects/{id}/generate` - Generate BRD
- `PUT /api/brds/{id}/edit` - Edit BRD with natural language
- `GET /api/brds/{id}` - Retrieve BRD
- `GET /api/brds/{id}/citations` - Get citation map

## License

MIT
