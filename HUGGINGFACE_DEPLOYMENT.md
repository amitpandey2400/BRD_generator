# Deploying BRD Generator to Hugging Face Spaces 🚀

This guide will help you deploy your BRD Generator application to Hugging Face Spaces.

## Prerequisites

1. **Hugging Face Account** - Sign up at https://huggingface.co/
2. **Gemini API Key** - Get free at https://ai.google.dev/
3. **Git** - Installed on your system

## Step-by-Step Deployment

### Step 1: Create a Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: `brd-generator` (or your preferred name)
   - **License**: MIT
   - **Select SDK**: Docker
   - **Space hardware**: CPU basic (free tier)
4. Click **"Create Space"**

### Step 2: Prepare Your Repository

1. **Initialize Git** (if not already done):
```bash
cd "C:\Users\devil\OneDrive\Desktop\Programming\Bussines manager"
git init
```

2. **Create .gitignore**:
```bash
# Copy the .gitignore content from below
```

3. **Update requirements.txt**:
   - Use the simplified `requirements_huggingface.txt` for deployment
   - Copy it as `requirements.txt` in your deployment branch

4. **Update database configuration**:
   - The app will use SQLite instead of PostgreSQL for Hugging Face
   - Update `alembic.ini` to use SQLite

### Step 3: Configure Environment Variables

In your Hugging Face Space settings:

1. Go to your Space → **Settings** → **Variables and secrets**
2. Add these secrets:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `SECRET_KEY`: A random secret string (generate with: `openssl rand -hex 32`)

Optional secrets:
   - `OPENAI_API_KEY`: If you want to use OpenAI instead
   - `DATABASE_URL`: For external PostgreSQL (if needed)

### Step 4: Update Files for Deployment

#### Update `alembic.ini`:
Change the database URL to use SQLite:
```ini
sqlalchemy.url = sqlite:///./brd_generator.db
```

#### Update `storage/database.py`:
Ensure it supports both PostgreSQL and SQLite:
```python
# Add this check in your database.py
if "sqlite" in settings.DATABASE_URL:
    engine = create_async_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_async_engine(settings.DATABASE_URL)
```

### Step 5: Push to Hugging Face

1. **Add Hugging Face remote**:
```bash
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/brd-generator
```

2. **Commit your files**:
```bash
git add .
git commit -m "Initial deployment to Hugging Face"
```

3. **Push to Hugging Face**:
```bash
git push hf main
```

### Step 6: Wait for Build

- Hugging Face will automatically build your Docker container
- Check the **Logs** section in your Space to monitor the build process
- First build may take 5-10 minutes

### Step 7: Access Your Application

Once deployed, your app will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/brd-generator
```

## Files Needed for Deployment

Make sure these files are in your repository:

- ✅ `Dockerfile` - Container configuration
- ✅ `requirements.txt` - Python dependencies (use lightweight version)
- ✅ `README_HUGGINGFACE.md` - Rename to `README.md` for your Space
- ✅ `main.py` - Application entry point
- ✅ `.env.example` - Example environment variables
- ✅ `alembic/` - Database migrations
- ✅ `static/` - Frontend files
- ✅ All Python modules (api/, brd_generator/, etc.)

## Troubleshooting

### Build Fails

1. **Check logs** in Hugging Face Space
2. **Simplify dependencies** - Remove heavy packages like `torch`, `transformers`
3. **Use SQLite** instead of PostgreSQL

### Application Crashes

1. **Check environment variables** are set correctly
2. **Verify Gemini API key** is valid
3. **Check database migrations** ran successfully

### Slow Performance

1. **Upgrade to GPU Space** (paid tier) for better performance
2. **Optimize AI calls** - reduce max_tokens, use caching
3. **Consider using Persistent Storage** for database

## Alternative: Quick Deployment with Docker

If you have Docker installed locally, test before deploying:

```bash
# Build Docker image
docker build -t brd-generator .

# Run container
docker run -p 7860:7860 \
  -e GEMINI_API_KEY=your_api_key \
  -e SECRET_KEY=your_secret_key \
  brd-generator
```

Visit http://localhost:7860

## Using Hugging Face Transformers (Optional)

To use Hugging Face's own models instead of Gemini:

1. Add `transformers` to requirements
2. Update `utils/ai_client.py` to support HF models
3. Use models like `facebook/bart-large-cnn` for text generation

## Production Considerations

For production deployment:

1. **Use External Database**: 
   - Railway.app (PostgreSQL)
   - Supabase
   - Neon.tech

2. **File Storage**:
   - AWS S3
   - Cloudinary
   - Spaces Persistent Storage (paid)

3. **Monitoring**:
   - Set up error tracking
   - Monitor API usage
   - Log analytics

4. **Security**:
   - Use strong SECRET_KEY
   - Validate all inputs
   - Rate limit API endpoints

## Cost Considerations

- **Hugging Face Spaces**: Free tier (CPU basic) - Limited resources
- **Gemini API**: 1,500 requests/day free
- **Upgrade Options**: 
  - CPU upgrade: $0.05/hour
  - GPU: Starting at $0.60/hour
  - Persistent storage: $5/month

## Support

If you encounter issues:
1. Check Hugging Face Spaces documentation
2. Review the logs in your Space
3. Test locally with Docker first
4. Ask in Hugging Face forums

## Next Steps

After successful deployment:
1. ✅ Test all features (create project, upload docs, generate BRD)
2. ✅ Share your Space with users
3. ✅ Monitor usage and performance
4. ✅ Collect feedback and iterate

Happy deploying! 🚀
