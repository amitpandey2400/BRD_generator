# Quick Start: Deploy to Hugging Face Spaces

## Summary (TL;DR)

```bash
# 1. Run preparation script
.\prepare_deployment.ps1

# 2. Create Space at https://huggingface.co/new-space (SDK: Docker)

# 3. Add remote and push
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
git add .
git commit -m "Deploy to Hugging Face"
git push hf main

# 4. Set environment variables in HF Space settings:
#    - GEMINI_API_KEY: your_key_here
#    - SECRET_KEY: random_secret_string
```

## What You Need

1. **Hugging Face Account** (free): https://huggingface.co/join
2. **Gemini API Key** (free): https://ai.google.dev/
3. **Git** installed on your computer

## Detailed Steps

### 1. Prepare Your Code

Run the preparation script:
```powershell
.\prepare_deployment.ps1
```

This will:
- ✅ Check Git installation
- ✅ Initialize repository
- ✅ Verify all deployment files exist
- ✅ Create necessary directories

### 2. Create Hugging Face Space

1. Go to: https://huggingface.co/new-space
2. Fill in:
   - **Space name**: `brd-generator` (or your choice)
   - **License**: MIT
   - **SDK**: Select **Docker** ⚠️ Important!
   - **Space hardware**: CPU basic (free)
3. Click "Create Space"

### 3. Get Your API Key

1. Visit: https://ai.google.dev/
2. Click "Get API Key"
3. Create project and generate key
4. Copy the key (starts with `AIza...`)

### 4. Connect and Push

```bash
# Add Hugging Face as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/brd-generator

# Stage all files
git add .

# Commit
git commit -m "Initial deployment to Hugging Face Spaces"

# Push to Hugging Face
git push hf main
```

### 5. Configure Environment Variables

1. Go to your Space on Hugging Face
2. Click **Settings** tab
3. Scroll to **"Variables and secrets"**
4. Add these secrets:

| Name | Value | Required |
|------|-------|----------|
| `GEMINI_API_KEY` | Your Gemini API key | ✅ Yes |
| `SECRET_KEY` | Any random string (32+ chars) | ✅ Yes |
| `DATABASE_URL` | `sqlite:///./brd_generator.db` | Auto-set |

To generate a secure SECRET_KEY:
```powershell
# Windows PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### 6. Wait for Build

- Building takes 5-10 minutes
- Watch the **App** tab for build logs
- You'll see: "Building..." → "Running..."

### 7. Access Your App

Your app will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/brd-generator
```

## Testing Your Deployment

1. Visit your Space URL
2. Click **"➕ Create Project"**
3. Enter:
   - Name: "Test Project"
   - Description: "Build a mobile app for e-commerce"
4. Go to **"🤖 Generate BRD"**
5. Select project and click "Generate"
6. Wait 20-30 seconds
7. View your generated BRD! 🎉

## Troubleshooting

### Build Failed

**Error**: Dependencies timeout
```bash
# Solution: Use lightweight requirements
git checkout requirements_huggingface.txt
git mv requirements_huggingface.txt requirements.txt
git commit -m "Use lightweight requirements"
git push hf main
```

### App Crashes

**Error**: `GEMINI_API_KEY not set`
- Go to Space Settings → Secrets
- Add `GEMINI_API_KEY` with your key
- App will restart automatically

### Database Error

**Error**: `Connection refused` or `async dialect not found`
```bash
# Add to Space secrets:
DATABASE_URL=sqlite+aiosqlite:///./brd_generator.db
```

### Slow Generation

- Normal! Free CPU tier is slower
- First request takes longer (cold start)
- Consider upgrading to faster hardware:
  - Settings → Hardware → CPU upgrade ($0.05/hr)

## Updating Your Deployment

To update your deployed app:

```bash
# Make changes locally
# Test locally first!

# Commit changes
git add .
git commit -m "Update: describe your changes"

# Push to Hugging Face
git push hf main

# App rebuilds automatically (5-10 min)
```

## Cost Breakdown

- **Hugging Face Space (CPU basic)**: FREE ✅
- **Gemini API**: 1,500 requests/day FREE ✅
- **Total**: $0.00/month 🎉

Upgrade options:
- **CPU upgrade**: $0.05/hour (~$36/month if 24/7)
- **GPU T4**: $0.60/hour (~$432/month if 24/7)
- **Persistent storage**: $5/month

## Next Steps

After deployment:

1. ✅ **Share your Space** - Send the link to users
2. ✅ **Add to your README** - Include usage examples
3. ✅ **Monitor usage** - Check Space analytics
4. ✅ **Collect feedback** - Iterate based on user input
5. ✅ **Star the Space** - Help others discover it

## Support

Need help?
- 📖 Read: `HUGGINGFACE_DEPLOYMENT.md` (detailed guide)
- 💬 Ask: Hugging Face Community forums
- 🐛 Report: Issues on your Space

## Example Spaces

Check out similar Spaces for inspiration:
- https://huggingface.co/spaces/gradio/chatbot
- https://huggingface.co/spaces/huggingface/text-generation

---

**Ready? Let's deploy! 🚀**

Run: `.\prepare_deployment.ps1` to start!
