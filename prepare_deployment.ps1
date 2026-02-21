# Deployment Preparation Script for Hugging Face Spaces
# Run this script to prepare your application for deployment

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   BRD Generator - Hugging Face Deployment" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Check Git
Write-Host "Step 1: Checking Git..." -ForegroundColor Yellow
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "  ✅ Git is installed" -ForegroundColor Green
} else {
    Write-Host "  ❌ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Step 2: Initialize Git repository
Write-Host "`nStep 2: Initializing Git repository..." -ForegroundColor Yellow
if (Test-Path .git) {
    Write-Host "  ✅ Git repository already initialized" -ForegroundColor Green
} else {
    git init
    Write-Host "  ✅ Git repository initialized" -ForegroundColor Green
}

# Step 3: Create necessary files
Write-Host "`nStep 3: Checking deployment files..." -ForegroundColor Yellow

$files = @(
    "Dockerfile",
    "requirements_huggingface.txt",
    "README_HUGGINGFACE.md",
    ".gitignore"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file missing" -ForegroundColor Red
    }
}

# Step 4: Copy lightweight requirements
Write-Host "`nStep 4: Using lightweight requirements..." -ForegroundColor Yellow
if (Test-Path "requirements_huggingface.txt") {
    Copy-Item "requirements_huggingface.txt" "requirements_deploy.txt" -Force
    Write-Host "  ✅ Created requirements_deploy.txt" -ForegroundColor Green
}

# Step 5: Create .env.example if not exists
Write-Host "`nStep 5: Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env.example") {
    Write-Host "  ✅ .env.example exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  .env.example not found" -ForegroundColor Yellow
}

# Step 6: Create storage directories
Write-Host "`nStep 6: Creating storage directories..." -ForegroundColor Yellow
$dirs = @("storage/documents", "storage/temp", "logs")
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        New-Item -ItemType File -Path "$dir/.gitkeep" -Force | Out-Null
    }
}
Write-Host "  ✅ Storage directories ready" -ForegroundColor Green

# Step 7: Instructions
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Next Steps" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "1. Create a Hugging Face Space:" -ForegroundColor White
Write-Host "   https://huggingface.co/new-space" -ForegroundColor Gray
Write-Host "   - SDK: Docker" -ForegroundColor Gray
Write-Host "   - Hardware: CPU basic (free)" -ForegroundColor Gray

Write-Host "`n2. Get your Gemini API key:" -ForegroundColor White
Write-Host "   https://ai.google.dev/" -ForegroundColor Gray

Write-Host "`n3. Add the Hugging Face remote:" -ForegroundColor White
Write-Host "   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME" -ForegroundColor Gray

Write-Host "`n4. Add environment variables in HF Space settings:" -ForegroundColor White
Write-Host "   - GEMINI_API_KEY: your-gemini-key" -ForegroundColor Gray
Write-Host "   - SECRET_KEY: $(openssl rand -hex 32)" -ForegroundColor Gray

Write-Host "`n5. Commit and push your code:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Deploy to Hugging Face Spaces'" -ForegroundColor Gray
Write-Host "   git push hf main" -ForegroundColor Gray

Write-Host "`n6. Wait for deployment (5-10 minutes)" -ForegroundColor White

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "For detailed instructions, see:" -ForegroundColor White
Write-Host "HUGGINGFACE_DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan
