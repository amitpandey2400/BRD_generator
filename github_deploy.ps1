# Quick GitHub Deployment Script
# Automates the process of pushing to GitHub

param(
    [string]$username = "",
    [string]$reponame = "brd-generator",
    [string]$message = "Initial commit: BRD Generator"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   GitHub Deployment Helper" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Git is installed
Write-Host "Checking Git installation..." -ForegroundColor Yellow
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed!" -ForegroundColor Red
    Write-Host "`nPlease install Git from:" -ForegroundColor Yellow
    Write-Host "https://git-scm.com/download/win`n" -ForegroundColor Cyan
    exit 1
}
Write-Host "✅ Git is installed: $(git --version)" -ForegroundColor Green

# Get GitHub username if not provided
if ($username -eq "") {
    Write-Host "`nGitHub Setup:" -ForegroundColor Yellow
    $username = Read-Host "Enter your GitHub username"
    if ($username -eq "") {
        Write-Host "❌ Username is required!" -ForegroundColor Red
        exit 1
    }
}

# Confirm repository name
Write-Host "`nRepository name: $reponame" -ForegroundColor Cyan
$confirm = Read-Host "Use this name? (y/n)"
if ($confirm -eq "n") {
    $reponame = Read-Host "Enter repository name"
}

# Initialize Git if needed
Write-Host "`n📦 Initializing Git repository..." -ForegroundColor Yellow
if (!(Test-Path .git)) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Check Git configuration
Write-Host "`n🔧 Checking Git configuration..." -ForegroundColor Yellow
$gitUserName = git config user.name
$gitUserEmail = git config user.email

if (!$gitUserName) {
    $userName = Read-Host "Enter your name for Git commits"
    git config user.name "$userName"
}
if (!$gitUserEmail) {
    $userEmail = Read-Host "Enter your email for Git commits"
    git config user.email "$userEmail"
}
Write-Host "✅ Git configured as: $(git config user.name) <$(git config user.email)>" -ForegroundColor Green

# Stage all files
Write-Host "`n📋 Staging files..." -ForegroundColor Yellow
git add .
$stagedFiles = git diff --cached --name-only
$fileCount = ($stagedFiles | Measure-Object).Count
Write-Host "✅ Staged $fileCount files" -ForegroundColor Green

# Show what will be committed
if ($fileCount -gt 0) {
    Write-Host "`nFiles to be committed:" -ForegroundColor Cyan
    $stagedFiles | Select-Object -First 10 | ForEach-Object {
        Write-Host "  + $_" -ForegroundColor Gray
    }
    if ($fileCount -gt 10) {
        Write-Host "  ... and $($fileCount - 10) more files" -ForegroundColor Gray
    }
}

# Commit
Write-Host "`n💾 Creating commit..." -ForegroundColor Yellow
git commit -m "$message"
Write-Host "✅ Committed successfully" -ForegroundColor Green

# Check if remote exists
$remoteExists = git remote | Select-String -Pattern "origin" -Quiet
if ($remoteExists) {
    Write-Host "`n⚠️  Remote 'origin' already exists" -ForegroundColor Yellow
    $remoteUrl = git remote get-url origin
    Write-Host "Current remote: $remoteUrl" -ForegroundColor Gray
    $updateRemote = Read-Host "Update remote URL? (y/n)"
    if ($updateRemote -eq "y") {
        git remote remove origin
        git remote add origin "https://github.com/$username/$reponame.git"
        Write-Host "✅ Remote updated" -ForegroundColor Green
    }
} else {
    Write-Host "`n🔗 Adding GitHub remote..." -ForegroundColor Yellow
    git remote add origin "https://github.com/$username/$reponame.git"
    Write-Host "✅ Remote added: https://github.com/$username/$reponame.git" -ForegroundColor Green
}

# Rename branch to main if needed
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    Write-Host "`n🌿 Renaming branch to 'main'..." -ForegroundColor Yellow
    git branch -M main
    Write-Host "✅ Branch renamed to main" -ForegroundColor Green
}

# Push to GitHub
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Ready to Push to GitHub!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Repository URL: https://github.com/$username/$reponame" -ForegroundColor Cyan
Write-Host "`nIMPORTANT:" -ForegroundColor Yellow
Write-Host "1. Make sure you've created the repository on GitHub" -ForegroundColor White
Write-Host "   → https://github.com/new" -ForegroundColor Gray
Write-Host "2. If prompted, use your GitHub Personal Access Token as password" -ForegroundColor White
Write-Host "   → https://github.com/settings/tokens" -ForegroundColor Gray

$push = Read-Host "`nPush to GitHub now? (y/n)"
if ($push -eq "y") {
    Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================" -ForegroundColor Cyan
        Write-Host "   ✅ SUCCESS!" -ForegroundColor Green
        Write-Host "========================================`n" -ForegroundColor Cyan
        Write-Host "Your code is now on GitHub!" -ForegroundColor Green
        Write-Host "`nRepository: https://github.com/$username/$reponame" -ForegroundColor Cyan
        Write-Host "`nNext steps:" -ForegroundColor Yellow
        Write-Host "1. Visit your repository to verify" -ForegroundColor White
        Write-Host "2. (Optional) Deploy to Hugging Face:" -ForegroundColor White
        Write-Host "   → https://huggingface.co/new-space" -ForegroundColor Gray
        Write-Host "   → Link to your GitHub repo" -ForegroundColor Gray
        Write-Host "   → Add GEMINI_API_KEY secret" -ForegroundColor Gray
        Write-Host "`n📖 See GITHUB_DEPLOYMENT.md for more details`n" -ForegroundColor Cyan
    } else {
        Write-Host "`n❌ Push failed!" -ForegroundColor Red
        Write-Host "`nCommon issues:" -ForegroundColor Yellow
        Write-Host "1. Repository doesn't exist on GitHub - Create it at https://github.com/new" -ForegroundColor White
        Write-Host "2. Authentication failed - Use Personal Access Token, not password" -ForegroundColor White
        Write-Host "3. Repository not empty - Use 'git pull origin main --allow-unrelated-histories' first" -ForegroundColor White
        Write-Host "`n📖 See GITHUB_DEPLOYMENT.md troubleshooting section`n" -ForegroundColor Cyan
    }
} else {
    Write-Host "`n To push manually, run:" -ForegroundColor Yellow
    Write-Host "git push -u origin main`n" -ForegroundColor Gray
}

Write-Host "========================================`n" -ForegroundColor Cyan
