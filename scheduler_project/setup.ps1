# Quick Setup Script for Task Scheduler
# Run this script to set up the Django application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Task Scheduler - Quick Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
$projectPath = "c:\Users\oussa\Desktop\Projet tut\scheduler_project"
Set-Location $projectPath
Write-Host "✓ Navigated to project directory" -ForegroundColor Green

# Install dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Error installing dependencies" -ForegroundColor Red
    exit 1
}

# Create migrations
Write-Host "`nCreating database migrations..." -ForegroundColor Yellow
python manage.py makemigrations scheduler
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Migrations created" -ForegroundColor Green
} else {
    Write-Host "✗ Error creating migrations" -ForegroundColor Red
}

# Apply migrations
Write-Host "`nApplying migrations to database..." -ForegroundColor Yellow
python manage.py migrate
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database initialized" -ForegroundColor Green
} else {
    Write-Host "✗ Error applying migrations" -ForegroundColor Red
    exit 1
}

# Create media directories
Write-Host "`nCreating media directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "media\samples" | Out-Null
New-Item -ItemType Directory -Force -Path "media\uploads" | Out-Null
Write-Host "✓ Media directories created" -ForegroundColor Green

# Copy sample datasets
Write-Host "`nCopying sample datasets..." -ForegroundColor Yellow
$parentPath = Split-Path -Parent $projectPath
if (Test-Path "$parentPath\dataset_facile.csv") {
    Copy-Item "$parentPath\dataset_facile.csv" "media\samples\" -Force
    Copy-Item "$parentPath\dataset_moyen.csv" "media\samples\" -Force
    Copy-Item "$parentPath\dataset_difficile.csv" "media\samples\" -Force
    Write-Host "✓ Sample datasets copied" -ForegroundColor Green
} else {
    Write-Host "⚠ Sample datasets not found (optional)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Create admin user (optional):" -ForegroundColor White
Write-Host "     python manage.py createsuperuser" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Start the development server:" -ForegroundColor White
Write-Host "     python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Open browser to:" -ForegroundColor White
Write-Host "     http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to create superuser
$createAdmin = Read-Host "Would you like to create an admin user now? (y/n)"
if ($createAdmin -eq 'y' -or $createAdmin -eq 'Y') {
    Write-Host "`nCreating admin user..." -ForegroundColor Yellow
    python manage.py createsuperuser
}

# Ask if user wants to start server
$startServer = Read-Host "`nWould you like to start the development server now? (y/n)"
if ($startServer -eq 'y' -or $startServer -eq 'Y') {
    Write-Host "`nStarting development server..." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    python manage.py runserver
} else {
    Write-Host "`nTo start the server later, run:" -ForegroundColor Yellow
    Write-Host "  python manage.py runserver" -ForegroundColor Gray
}
