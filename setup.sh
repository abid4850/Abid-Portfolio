#!/bin/bash

# Django Portfolio Blog - Quick Setup Script
# Linux/Mac Bash Script to set up the blog system in one go

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Django Portfolio Blog - Automated Setup Script              ║"
echo "║  Version 1.0 - February 8, 2024                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ ERROR: manage.py not found!"
    echo "Please run this script from the project root directory."
    echo ""
    exit 1
fi

echo "✓ Project root directory verified"
echo ""

# Step 1: Run Migrations
echo "════════════════════════════════════════════════════════════════"
echo "STEP 1/4: Applying Database Migrations"
echo "════════════════════════════════════════════════════════════════"
echo ""
python manage.py migrate portfolio

if [ $? -ne 0 ]; then
    echo "❌ Migration failed!"
    exit 1
fi

echo ""
echo "✓ Migrations applied successfully"
echo ""

# Step 2: Check for existing superuser
echo "════════════════════════════════════════════════════════════════"
echo "STEP 2/4: Checking for Superuser Account"
echo "════════════════════════════════════════════════════════════════"
echo ""

python manage.py shell -c "from django.contrib.auth.models import User; count = User.objects.count(); print(f'Existing users: {count}')"

echo ""
read -p "Do you want to create a superuser? (y/n): " create_admin

if [[ "$create_admin" =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
    if [ $? -ne 0 ]; then
        echo "❌ Superuser creation failed!"
        exit 1
    fi
    echo ""
    echo "✓ Superuser created successfully"
else
    echo "⚠ Skipping superuser creation"
fi

echo ""

# Step 3: Collect static files (optional but recommended)
echo "════════════════════════════════════════════════════════════════"
echo "STEP 3/4: Collecting Static Files (Optional)"
echo "════════════════════════════════════════════════════════════════"
echo ""

read -p "Do you want to collect static files? (y/n): " collect_static

if [[ "$collect_static" =~ ^[Yy]$ ]]; then
    python manage.py collectstatic --noinput
    if [ $? -ne 0 ]; then
        echo "⚠ Warning: Static files collection had issues"
    fi
    echo "✓ Static files collected"
else
    echo "⚠ Skipping static files collection"
fi

echo ""

# Step 4: Start development server
echo "════════════════════════════════════════════════════════════════"
echo "STEP 4/4: Starting Development Server"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "✓ Setup complete! Starting development server..."
echo ""
echo "📌 Important URLs:"
echo "   - Admin Panel:     http://localhost:8000/admin/"
echo "   - Blog List:       http://localhost:8000/blogs/"
echo "   - Home:            http://localhost:8000/"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python manage.py runserver
