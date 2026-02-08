@echo off
REM Django Portfolio Blog - Quick Setup Script
REM Windows Batch Script to set up the blog system in one go

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  Django Portfolio Blog - Automated Setup Script              ║
echo ║  Version 1.0 - February 8, 2024                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if we're in the right directory
if not exist "manage.py" (
    echo ❌ ERROR: manage.py not found!
    echo Please run this script from the project root directory.
    echo.
    pause
    exit /b 1
)

echo ✓ Project root directory verified
echo.

REM Step 1: Run Migrations
echo ════════════════════════════════════════════════════════════════
echo STEP 1/4: Applying Database Migrations
echo ════════════════════════════════════════════════════════════════
echo.
python manage.py migrate portfolio

if %errorlevel% neq 0 (
    echo ❌ Migration failed!
    pause
    exit /b 1
)

echo.
echo ✓ Migrations applied successfully
echo.

REM Step 2: Check for existing superuser
echo ════════════════════════════════════════════════════════════════
echo STEP 2/4: Checking for Superuser Account
echo ════════════════════════════════════════════════════════════════
echo.

python manage.py shell -c "from django.contrib.auth.models import User; count = User.objects.count(); print(f'Existing users: {count}')"

echo.
set /p create_admin="Do you want to create a superuser? (y/n): "

if /i "%create_admin%"=="y" (
    python manage.py createsuperuser
    if %errorlevel% neq 0 (
        echo ❌ Superuser creation failed!
        pause
        exit /b 1
    )
    echo.
    echo ✓ Superuser created successfully
) else (
    echo ⚠ Skipping superuser creation
)

echo.

REM Step 3: Collect static files (optional but recommended)
echo ════════════════════════════════════════════════════════════════
echo STEP 3/4: Collecting Static Files (Optional)
echo ════════════════════════════════════════════════════════════════
echo.

set /p collect_static="Do you want to collect static files? (y/n): "

if /i "%collect_static%"=="y" (
    python manage.py collectstatic --noinput
    if %errorlevel% neq 0 (
        echo ⚠ Warning: Static files collection had issues
    )
    echo ✓ Static files collected
) else (
    echo ⚠ Skipping static files collection
)

echo.

REM Step 4: Start development server
echo ════════════════════════════════════════════════════════════════
echo STEP 4/4: Starting Development Server
echo ════════════════════════════════════════════════════════════════
echo.
echo ✓ Setup complete! Starting development server...
echo.
echo 📌 Important URLs:
echo    - Admin Panel:     http://localhost:8000/admin/
echo    - Blog List:       http://localhost:8000/blogs/
echo    - Home:            http://localhost:8000/
echo.
echo Press CTRL+C to stop the server
echo.
REM Wait a moment for user to read
timeout /t 2

python manage.py runserver

pause
