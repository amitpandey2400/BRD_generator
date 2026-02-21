# 🚀 Quick Start: GitHub Deployment (5 Minutes)

## Step-by-Step Commands

### 1️⃣ Install Git (if needed)
Download and install: https://git-scm.com/download/win

### 2️⃣ Create GitHub Repository
Go to: https://github.com/new
- Name: `brd-generator`
- Public or Private
- ❌ Don't add README, .gitignore, or license
- Click "Create repository"

### 3️⃣ Run Automated Script (EASIEST)
```powershell
.\github_deploy.ps1
```
Follow the prompts and you're done! ✅

---

## OR: Manual Deployment

### 3️⃣ Configure Git
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4️⃣ Initialize and Commit
```powershell
# Initialize repository
git init

# Stage all files
git add .

# Create first commit
git commit -m "Initial commit: BRD Generator"
```

### 5️⃣ Connect to GitHub
Replace `YOUR_USERNAME` with your GitHub username:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/brd-generator.git
git branch -M main
git push -u origin main
```

### 6️⃣ Enter Credentials
When prompted:
- **Username**: Your GitHub username
- **Password**: Use Personal Access Token (NOT your password)
  - Get token at: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Select: `repo` (all permissions)
  - Copy the token

---

## ✅ Verify Success

Visit: `https://github.com/YOUR_USERNAME/brd-generator`

You should see all your files! 🎉

---

## 🔄 Future Updates

When you make changes:
```powershell
git add .
git commit -m "Description of changes"
git push
```

---

## 🚀 Deploy to Hugging Face (Optional)

### Option 1: Link GitHub Repository

1. Go to: https://huggingface.co/new-space
2. Choose:
   - SDK: **Docker**
   - Link to GitHub repository: `YOUR_USERNAME/brd-generator`
3. Add secrets in Space settings:
   - `GEMINI_API_KEY`: Get from https://ai.google.dev/
   - `SECRET_KEY`: Any random 32-character string
4. Auto-deploys on every Git push! 🎉

### Option 2: Manual HF Git

```powershell
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/brd-generator
git push hf main
```

---

## 🐛 Common Issues

### "Repository not found"
→ Make sure you created it on GitHub first at https://github.com/new

### "Authentication failed"  
→ Use Personal Access Token, not password
→ Get at: https://github.com/settings/tokens

### "Git not found"
→ Install Git: https://git-scm.com/download/win
→ Restart PowerShell after installing

---

## 📚 Full Documentation

- **Detailed guide**: `GITHUB_DEPLOYMENT.md`
- **Hugging Face guide**: `HUGGINGFACE_DEPLOYMENT.md`
- **Quick HF deploy**: `QUICKSTART_DEPLOYMENT.md`

---

## 💡 Pro Tips

1. **Test before push**: Run `python main.py` locally first
2. **Check status**: `git status` shows what will be committed  
3. **View changes**: `git diff` shows what changed
4. **Commit often**: Small, frequent commits are better
5. **Use branches**: `git checkout -b feature-name` for new features

---

## 💰 Cost

- GitHub: **FREE** ✅
- Hugging Face: **FREE** (CPU basic) ✅  
- Gemini API: **FREE** (1,500 req/day) ✅
- **Total: $0.00/month** 🎉

---

## ⚡ Quick Commands

```powershell
# Automated deployment
.\github_deploy.ps1

# Check what changed
git status

# Quick commit & push
git add . && git commit -m "Update" && git push

# View repository URL
git remote -v

# Pull latest changes
git pull

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

**Ready? Run:** `.\github_deploy.ps1` 🚀
