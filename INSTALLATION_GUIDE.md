# 🚀 Complete Installation Guide

## Prerequisites Installation

### 1. Install Python 3.11+

**Download Python:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or later (Python 3.12 recommended)
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Click "Install Now"

**Verify Installation:**
```powershell
python --version
# Should show: Python 3.11.x or 3.12.x
```

### 2. Install PostgreSQL (Database)

**Download PostgreSQL:**
1. Go to https://www.postgresql.org/download/windows/
2. Download the Windows installer (version 15 or 16)
3. Run the installer
4. Remember the password you set for the 'postgres' user
5. Keep default port (5432)

**Create Database:**
```powershell
# Open Command Prompt or PowerShell
psql -U postgres
# Enter your postgres password when prompted

# In PostgreSQL prompt:
CREATE DATABASE brd_generator;
\q
```

### 3. Install Redis (Optional - for background tasks)

**Using Chocolatey (Recommended):**
```powershell
# First install Chocolatey (run as Administrator):
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install Redis:
choco install redis-64
```

**Alternative - Memurai (Redis for Windows):**
1. Download from https://www.memurai.com/get-memurai
2. Install and start the service

**Or Skip Redis for Now:**
- Redis is only needed for Celery background tasks
- You can run the project without it initially

---

## Project Setup

### Step 1: Create Virtual Environment

```powershell
cd "c:\Users\devil\OneDrive\Desktop\Programming\Bussines manager"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try activating again
```

### Step 2: Install Python Dependencies

```powershell
# Make sure virtual environment is activated (you should see (venv) in prompt)
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# If you encounter errors with specific packages, try:
pip install --no-cache-dir -r requirements.txt
```

**Common Installation Issues:**

**If you get errors with pgvector:**
```powershell
# Skip pgvector for now (it's for future use)
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic openai langchain redis celery python-dotenv aiofiles httpx pandas
```

**If you get errors with spaCy:**
```powershell
# Install spaCy separately
pip install spacy==3.7.2
python -m spacy download en_core_web_sm
```

### Step 3: Configure Environment Variables

```powershell
# Copy the example environment file
copy .env.example .env

# Edit .env file with your API keys
notepad .env
```

**Required in .env:**
```
OPENAI_API_KEY=sk-your-actual-openai-key-here
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/brd_generator
SECRET_KEY=your-secret-key-change-this
```

**Optional (can add later):**
```
GMAIL_CLIENT_ID=your-gmail-client-id
GMAIL_CLIENT_SECRET=your-gmail-secret
SLACK_BOT_TOKEN=xoxb-your-slack-token
FIREFLIES_API_KEY=your-fireflies-key
REDIS_URL=redis://localhost:6379/0
```

### Step 4: Initialize Database

```powershell
# Make sure PostgreSQL is running and database is created

# Run database migrations
alembic upgrade head

# If alembic command not found, try:
python -m alembic upgrade head
```

### Step 5: Create Required Directories

```powershell
# Create storage directories
mkdir -p storage\documents
mkdir -p storage\temp
mkdir -p logs
```

---

## Running the Application

### Start the Server

```powershell
# Make sure virtual environment is activated
python main.py
```

You should see:
```
🚀 BRD Generator v1.0.0 started
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Access the Application

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Quick Test

### Test the API:

```powershell
# In a new PowerShell window, test the health endpoint:
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Should return:
# status   : healthy
# database : connected
# redis    : connected
```

### Create Your First Project:

```powershell
# Create a test project
$body = @{
    name = "Test Project"
    description = "My first BRD project"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/projects" -Method POST -Body $body -ContentType "application/json"
```

---

## Optional: Start Background Worker (Celery)

If you installed Redis:

```powershell
# In a new terminal, with virtual environment activated:
celery -A celery_tasks worker -l info --pool=solo
```

Note: Use `--pool=solo` on Windows

---

## Troubleshooting

### Python Not Found
- Reinstall Python and check "Add to PATH"
- Restart your terminal after installation
- Try `py` instead of `python`

### PostgreSQL Connection Failed
- Verify PostgreSQL is running: `pg_ctl status`
- Check password in .env matches your postgres password
- Ensure database 'brd_generator' exists

### OpenAI API Errors
- Verify your API key is valid
- Check you have credits on your OpenAI account
- Ensure no spaces in the API key in .env

### Import Errors
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`
- Try installing packages individually

### Port Already in Use
- Change port in .env: `PORT=8001`
- Or kill process using port 8000:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
  ```

---

## Minimal Installation (Without Optional Components)

If you want to start with just the essentials:

### Required:
1. ✅ Python 3.11+
2. ✅ PostgreSQL
3. ✅ OpenAI API Key
4. ✅ Project dependencies

### Optional (can add later):
- ❌ Redis (only for background tasks)
- ❌ Gmail API (only for email ingestion)
- ❌ Slack API (only for Slack ingestion)
- ❌ Fireflies API (only for meeting transcripts)

You can start with just document upload functionality!

---

## Next Steps After Installation

1. ✅ Open http://localhost:8000/docs
2. ✅ Create a project via API
3. ✅ Upload a document
4. ✅ Generate your first BRD
5. ✅ Read QUICKSTART.md for detailed usage

---

## Getting Help

- Check if all services are running: PostgreSQL, Redis (optional)
- Ensure virtual environment is activated (you see `(venv)` in terminal)
- Review error messages carefully
- Check the logs in `logs/app.log`

---

## Summary Checklist

- [ ] Python 3.11+ installed and in PATH
- [ ] PostgreSQL installed and running
- [ ] Database 'brd_generator' created
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] .env file configured with at least OPENAI_API_KEY
- [ ] Database migrations run successfully
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000/docs

**Once all checked, you're ready to generate BRDs!** 🎉
