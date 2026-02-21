# BRD Generator - Quick Start Guide

**🎉 Live Demo**: https://huggingface.co/spaces/2Amit4/brd-generator

## Installation

1. **Clone the repository**
   ```bash
   cd "c:\Users\devil\OneDrive\Desktop\Programming\Bussines manager"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   - OpenAI API key (required)
   - Gmail API credentials (optional)
   - Slack API tokens (optional)
   - Fireflies API key (optional)

5. **Set up database**
   
   Install PostgreSQL and create a database:
   ```sql
   CREATE DATABASE brd_generator;
   ```
   
   Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://postgres:password@localhost:5432/brd_generator
   ```

6. **Run migrations**
   ```bash
   alembic upgrade head
   ```

## Running the Application

### Start the API server:
```bash
python main.py
```

The API will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

## Basic Usage

### 1. Create a Project
```bash
curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "Project description"
  }'
```

### 2. Ingest Data
```bash
curl -X POST "http://localhost:8000/api/projects/{project_id}/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "sources": {
      "documents": ["path/to/document.pdf"]
    }
  }'
```

### 3. Process Data
```bash
curl -X POST "http://localhost:8000/api/projects/{project_id}/process"
```

### 4. Generate BRD
```bash
curl -X POST "http://localhost:8000/api/projects/{project_id}/generate-brd"
```

### 5. Download BRD
```bash
curl "http://localhost:8000/api/brds/{brd_id}/download" -o brd.md
```

### 6. Edit BRD
```bash
curl -X PUT "http://localhost:8000/api/brds/{brd_id}/edit" \
  -H "Content-Type: application/json" \
  -d '{
    "edit_request": "Add a section about data privacy requirements"
  }'
```

## Configuration

### Gmail Integration
1. Go to Google Cloud Console
2. Create OAuth 2.0 credentials
3. Download credentials.json
4. Place in project root
5. Run authentication flow on first use

### Slack Integration
1. Create Slack App
2. Add required scopes (channels:history, channels:read, users:read)
3. Install to workspace
4. Copy tokens to .env

### Fireflies Integration
1. Sign up at fireflies.ai
2. Get API key from settings
3. Add to .env

## Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│                  [Future Implementation]                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI REST API                        │
│  ┌──────────┬──────────┬──────────┬──────────────────┐ │
│  │ Projects │   BRDs   │  Data    │  Authentication  │ │
│  │          │          │  Sources │                  │ │
│  └──────────┴──────────┴──────────┴──────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              BRD Orchestrator (Core Logic)               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Data Ingestion → Filtering → Extraction →        │  │
│  │  → Conflict Detection → BRD Generation → Editing  │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│   Gmail API  │ │  Slack API  │ │ Fireflies API│
└──────────────┘ └─────────────┘ └──────────────┘
         │               │               │
         └───────────────┼───────────────┘
                         ▼
              ┌────────────────────┐
              │   PostgreSQL DB    │
              │   + pgvector       │
              └────────────────────┘
```

## Key Features

✓ Multi-channel data ingestion (Gmail, Slack, Fireflies, Documents)
✓ Intelligent noise filtering using AI
✓ Automated requirement extraction
✓ Structured BRD generation
✓ Natural language editing
✓ Citation and traceability
✓ Conflict detection
✓ Sentiment analysis
✓ RESTful API

## Troubleshooting

### Database connection errors
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists

### API key errors
- Verify OpenAI API key is valid
- Check API key has sufficient credits
- Ensure .env file is loaded

### Import errors
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

## Next Steps

1. Implement frontend dashboard (React)
2. Add user authentication and authorization
3. Implement real-time progress updates via WebSockets
4. Add export to PDF/Word formats
5. Implement collaborative editing
6. Add more data source integrations

## Support

For issues or questions, please check:
- API Documentation: http://localhost:8000/docs
- README.md for detailed information
- Create an issue on GitHub

## License

MIT License - See LICENSE file for details
