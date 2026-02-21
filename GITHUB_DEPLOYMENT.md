# Deploying BRD Generator to GitHub 🚀

Complete guide to deploy your BRD Generator to GitHub repository and optionally to Hugging Face Spaces.

---

## 📋 Prerequisites

1. **GitHub Account** - Sign up at https://github.com/join (FREE)
2. **Git installed** - Download: https://git-scm.com/download/win
3. **Gemini API Key** (for deployment) - Get at https://ai.google.dev/

---

## Part 1: Deploy to GitHub Repository

### Step 1: Install Git (if not installed)

1. Download Git for Windows: https://git-scm.com/download/win
2. Run the installer with default settings
3. Verify installation:
```powershell
git --version
```

### Step 2: Configure Git

```powershell
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Create GitHub Repository

**Option A: Via GitHub Website (Recommended)**

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name**: `brd-generator` (or your choice)
   - **Description**: "AI-powered Business Requirements Document Generator"
   - **Visibility**: Public (for free Hugging Face deployment) or Private
   - ❌ **Don't check** "Add a README file"
   - ❌ **Don't add** .gitignore or license (we have them)
3. Click **"Create repository"**

**Option B: Via GitHub CLI**

```powershell
# Install GitHub CLI first: https://cli.github.com/
gh repo create brd-generator --public --source=. --remote=origin
```

### Step 4: Initialize Local Repository

In your project folder:

```powershell
# Navigate to your project
cd "C:\Users\devil\OneDrive\Desktop\Programming\Bussines manager"

# Initialize Git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: BRD Generator with Gemini AI"
```

### Step 5: Connect to GitHub and Push

Replace `YOUR_USERNAME` with your GitHub username:

```powershell
# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/brd-generator.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 6: Verify on GitHub

1. Go to: `https://github.com/YOUR_USERNAME/brd-generator`
2. You should see all your files!

---

## Part 2: Deploy to Hugging Face from GitHub (Optional)

Now that your code is on GitHub, deploy to Hugging Face Spaces:

### Step 1: Create Hugging Face Space

1. Go to: https://huggingface.co/new-space
2. Fill in:
   - **Space name**: `brd-generator`
   - **License**: MIT
   - **Select SDK**: **Docker** ⚠️ Important!
   - **Space hardware**: CPU basic (FREE)
   - ✅ **Check** "Link to a GitHub repository"
3. Enter your GitHub repo: `YOUR_USERNAME/brd-generator`
4. Click **"Create Space"**

### Step 2: Configure Environment Variables

1. In your Space, click **Settings**
2. Scroll to **"Repository secrets"**
3. Add these secrets:

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `GEMINI_API_KEY` | Your Gemini API key | https://ai.google.dev/ |
| `SECRET_KEY` | Random 32+ character string | See below |
| `DATABASE_URL` | `sqlite:///./brd_generator.db` | Auto for HF |

**Generate SECRET_KEY:**
```powershell
# PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### Step 3: Auto-Deploy Setup

Hugging Face will automatically:
- ✅ Detect the `Dockerfile`
- ✅ Build your container
- ✅ Deploy your app
- ✅ Update when you push to GitHub

Every time you push to GitHub, Hugging Face rebuilds automatically!

### Step 4: Wait for Deployment

- First build: 5-10 minutes
- Watch progress in Space → **App** tab
- Status: "Building..." → "Running..."

### Step 5: Access Your App

Your app will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/brd-generator
```

---

## 📝 Important Files for Deployment

### Files You Need (Already Created)

✅ **Dockerfile** - Container configuration
✅ **requirements_huggingface.txt** - Lightweight dependencies
✅ `.gitignore` - Files to exclude from Git
✅ `README_HUGGINGFACE.md` - Documentation

### Optional: Update README for GitHub

Rename `README_HUGGINGFACE.md` to `README.md`:

```powershell
# Backup current README
mv README.md README_LOCAL.md

# Use Hugging Face README as main
mv README_HUGGINGFACE.md README.md

# Commit
git add .
git commit -m "Update README for GitHub"
git push origin main
```

---

## 🔄 Updating Your Deployment

### Making Changes

```powershell
# Make your code changes
# Test locally first!

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add: describe what you changed"

# Push to GitHub
git push origin main

# Hugging Face auto-deploys in 5-10 minutes!
```

### Quick Update Commands

```powershell
# Check status
git status

# See changes
git diff

# Commit all changes
git add . && git commit -m "Update: description" && git push

# View commit history
git log --oneline
```

---

## 🌿 Branching Strategy (Optional)

For safer deployments:

```powershell
# Create development branch
git checkout -b develop

# Make changes, test them
# Commit to develop branch
git add .
git commit -m "Feature: new feature"
git push origin develop

# When ready, merge to main
git checkout main
git merge develop
git push origin main
```

---

## 📦 Project Structure for GitHub

```
brd-generator/
├── .git/                      # Git repository
├── .gitignore                 # Excluded files
├── Dockerfile                 # For Hugging Face deployment
├── requirements.txt           # Python dependencies
├── requirements_huggingface.txt  # Lightweight version
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
├── main.py                   # Application entry
├── .env.example              # Example environment variables
├── alembic.ini               # Database migrations config
├── api/                      # API routes
├── brd_generator/            # BRD generation logic
├── config/                   # Configuration
├── data_ingestion/           # Data ingestion modules
├── processing/               # AI processing
├── storage/                  # Database models
├── static/                   # Frontend (HTML/CSS/JS)
├── utils/                    # Utility functions
├── tests/                    # Test files
└── alembic/                  # Migration files
```

---

## 🔒 Security Best Practices

### Never Commit Secrets!

Already protected by `.gitignore`:
- ✅ `.env` - Environment variables
- ✅ `*.db` - Database files
- ✅ `.venv/` - Virtual environment
- ✅ `logs/` - Log files
- ✅ API keys

### If You Accidentally Committed Secrets:

```powershell
# Remove from Git history (DANGER!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (rewrites history)
git push origin --force --all

# IMPORTANT: Rotate your API keys immediately!
```

---

## 🐛 Troubleshooting

### Issue: Git not found

**Error**: `git: command not found`

**Solution**:
1. Install Git: https://git-scm.com/download/win
2. Restart PowerShell
3. Verify: `git --version`

### Issue: Authentication Failed

**Error**: `remote: Support for password authentication was removed`

**Solution**: Use Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (all)
4. Click "Generate token"
5. Copy token
6. Use token as password when Git asks

**Or use GitHub CLI** (easier):
```powershell
# Install: https://cli.github.com/
gh auth login
```

### Issue: Large Files

**Error**: `file is xxx MB; this exceeds GitHub's file size limit of 100 MB`

**Solution**:
```powershell
# Find large files
git ls-files | xargs -I{} git ls-tree -r --name-only HEAD | xargs -I{} du -h "{}"

# Remove from tracking
git rm --cached large_file.bin

# Add to .gitignore
echo "large_file.bin" >> .gitignore

# Use Git LFS for large files: https://git-lfs.github.com/
```

### Issue: Merge Conflicts

**Error**: `CONFLICT (content): Merge conflict in file.py`

**Solution**:
```powershell
# See conflicts
git status

# Edit files to resolve conflicts
# Look for <<<<<<< HEAD markers

# After fixing
git add .
git commit -m "Resolve merge conflict"
git push
```

---

## 💰 Cost Breakdown

- **GitHub Repository**: FREE ✅
  - Unlimited public repos
  - Unlimited private repos
  - GitHub Actions: 2,000 minutes/month free

- **Hugging Face Space**: FREE ✅
  - CPU basic tier
  - 7GB RAM
  - Auto-deploy from GitHub

- **Gemini API**: FREE ✅
  - 1,500 requests/day
  - No credit card required

**Total**: $0.00/month 🎉

---

## 🎯 Quick Commands Reference

```powershell
# Initialize & first push
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/brd-generator.git
git branch -M main
git push -u origin main

# Daily workflow
git pull                           # Get latest changes
git add .                          # Stage changes
git commit -m "Description"        # Commit
git push                           # Push to GitHub

# Branch management
git branch feature-name            # Create branch
git checkout feature-name          # Switch branch
git merge feature-name             # Merge branch
git branch -d feature-name         # Delete branch

# Undo changes
git reset --hard HEAD              # Discard all changes
git reset --soft HEAD~1            # Undo last commit
git checkout -- file.py            # Discard file changes

# Information
git status                         # Check status
git log --oneline                  # View commits
git remote -v                      # View remotes
git diff                           # See changes
```

---

## 📚 Additional Resources

- **Git Tutorial**: https://git-scm.com/docs/gittutorial
- **GitHub Docs**: https://docs.github.com/
- **Hugging Face Spaces**: https://huggingface.co/docs/hub/spaces
- **GitHub Actions**: https://docs.github.com/en/actions

---

## ✅ Checklist

### Before Pushing to GitHub:
- [ ] `.env` file is in `.gitignore`
- [ ] No API keys in code
- [ ] Large files excluded
- [ ] README.md updated
- [ ] License added

### After Pushing to GitHub:
- [ ] Repository is public/private as intended
- [ ] README displays correctly
- [ ] All files uploaded
- [ ] Clone and test in clean directory

### For Hugging Face Deployment:
- [ ] Dockerfile exists
- [ ] Lightweight requirements.txt
- [ ] Environment secrets configured
- [ ] Space linked to GitHub repo
- [ ] Auto-deploy working

---

## 🚀 You're Ready!

Follow the steps above to:
1. ✅ Push your code to GitHub
2. ✅ Deploy to Hugging Face Spaces (optional)
3. ✅ Share with the world!

**Questions?** Check the troubleshooting section or GitHub's documentation.

Happy deploying! 🎉
