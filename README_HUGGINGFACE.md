---
title: BRD Generator
emoji: 📄
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# BRD Generator 🚀

An AI-powered Business Requirements Document (BRD) Generator that helps you create professional BRDs in minutes.

## Features

- 📂 **Project Management** - Organize multiple business initiatives
- 📄 **Document Upload** - Support for Word, PDF, and text files
- 🤖 **AI Analysis** - Automatic requirement extraction using Google Gemini
- 📋 **Professional BRDs** - Generate complete, formatted documents
- ✏️ **Review & Edit** - AI-assisted editing capabilities
- 💾 **Export & Share** - Download as markdown or text

## How to Use

1. **Create a Project** - Start by creating a new project with a name and description
2. **Upload Documents** (Optional) - Add any relevant documents with project requirements
3. **Generate BRD** - Let AI analyze your project and generate a comprehensive BRD
4. **Download** - Export your professional business requirements document

## Technology Stack

- **Backend**: FastAPI with Python
- **Database**: PostgreSQL (SQLite for demo)
- **AI**: Google Gemini API (free tier)
- **Frontend**: HTML/CSS/JavaScript
- **Deployment**: Docker on Hugging Face Spaces

## Local Development

```bash
# Clone the repository
git clone <your-repo>
cd brd-generator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run database migrations
alembic upgrade head

# Start the application
python main.py
```

Visit `http://localhost:8000` to access the application.

## Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (get free at https://ai.google.dev/)
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for session management

## License

MIT License - See LICENSE file for details

## Credits

Built with ❤️ using FastAPI, Google Gemini AI, and modern web technologies.
