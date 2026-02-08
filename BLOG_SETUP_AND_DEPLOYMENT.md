# Django Portfolio Blog - Setup & Deployment Guide

## Overview

This guide provides comprehensive instructions to set up and deploy the blog feature on your Django portfolio website. The blog system includes a Blog model with author support, admin interface, and responsive templates.

---

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Database Migrations](#database-migrations)
3. [Superuser Creation](#superuser-creation)
4. [Creating Blog Posts](#creating-blog-posts)
5. [Testing Locally](#testing-locally)
6. [Deployment to Production](#deployment-to-production)
7. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### 1.1 Install Required Dependencies

```bash
# Navigate to your project directory
cd d:\Websites\ and\ apps\abid_portfolio

# Install required packages (if not already installed)
pip install django pillow
```

### 1.2 Verify Project Structure

Ensure your project has the following structure:

```
abid_portfolio/
├── abid_portfolio/          # Main project folder
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── portfolio/               # App folder
│   ├── models.py           # Contains Blog model
│   ├── admin.py            # Admin configuration
│   ├── views.py            # Blog views
│   ├── urls.py             # URL routing
│   ├── migrations/         # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_blog.py
│   │   ├── 0003_blog_image.py
│   │   └── 0004_blog_author_updated_at.py
│   └── templates/          # HTML templates
│       └── portfolio/
│           ├── blogs.html
│           └── blog_detail.html
├── manage.py
└── requirements.txt
```

---

## Database Migrations

### 2.1 Apply All Migrations

```bash
# Navigate to project directory
cd d:\Websites\ and\ apps\abid_portfolio

# Apply all pending migrations
python manage.py migrate

# Output should show:
# Applying portfolio.0004_blog_author_updated_at... OK
```

### 2.2 Check Migration Status

```bash
# View all applied migrations
python manage.py showmigrations
```

If you see any unapplied migrations, run:

```bash
python manage.py migrate portfolio
```

---

## Superuser Creation

### 3.1 Create Superuser Account (First Time)

```bash
# Navigate to project directory
cd d:\Websites\ and\ apps\abid_portfolio

# Create a new superuser (admin account)
python manage.py createsuperuser
```

When prompted, enter:

```
Username: admin
Email address: your-email@example.com
Password: [strong password - must contain letters, numbers, special chars]
Password (again): [confirm password]
Superuser created successfully.
```

**Important Notes:**
- Use a strong password with at least 8 characters
- Include uppercase, lowercase, numbers, and special characters
- Store credentials securely (password manager recommended)
- Never commit password to version control

### 3.2 Verify Superuser Creation

```bash
# Access Django shell to verify
python manage.py shell

# In the shell:
>>> from django.contrib.auth.models import User
>>> User.objects.all()
<QuerySet [<User: admin>]>
>>> exit()
```

---

## Creating Blog Posts

### 4.1 Access Django Admin Panel

1. **Start Development Server:**
   ```bash
   cd d:\Websites\ and\ apps\abid_portfolio
   python manage.py runserver
   ```

2. **Visit Admin Page:**
   ```
   http://localhost:8000/admin/
   ```

3. **Login with Superuser Credentials:**
   - Username: `admin`
   - Password: [Your superuser password]

### 4.2 Add a Blog Post via Admin

1. Click on **"Blogs"** in the admin panel (under Portfolio)
2. Click **"+ Add Blog"** button
3. Fill in the following fields:

   | Field | Description | Required |
   |-------|-------------|----------|
   | **Title** | Blog post title | Yes |
   | **Slug** | URL-friendly version (auto-generated) | Yes |
   | **Author** | Select from registered users | No* |
   | **Excerpt** | Short summary (optional) | No |
   | **Content** | Full blog post content (HTML supported) | Yes |
   | **Image** | Featured image for the blog | No |
   | **Published Date** | When to publish the post | No |

   *While optional, it's recommended to set an author for each post.

4. Click **"Save"** to create the post

### 4.3 Example Blog Post

```
Title: Getting Started with Django
Slug: getting-started-with-django
Author: admin
Excerpt: Learn the basics of Django framework
Content: <h2>Introduction</h2>
         <p>Django is a powerful web framework...</p>
         [Your HTML content here]
Published Date: 2024-02-08
```

### 4.4 View Published Posts

- **Blog List:** `http://localhost:8000/blogs/`
- **Blog Detail:** `http://localhost:8000/blogs/getting-started-with-django/`

---

## Testing Locally

### 5.1 Start Development Server

```bash
cd d:\Websites\ and\ apps\abid_portfolio
python manage.py runserver
```

Then visit: `http://localhost:8000/`

### 5.2 Test Blog Features

1. **Blog List Page:**
   - Visit: `http://localhost:8000/blogs/`
   - Verify all blog posts display correctly
   - Check author name appears with each post
   - Test date formatting

2. **Blog Detail Page:**
   - Click on any blog post
   - Verify full content displays
   - Check author information is visible
   - Test image rendering (if included)

3. **Admin Interface:**
   - Visit: `http://localhost:8000/admin/`
   - Test creating a new blog post
   - Test editing existing posts
   - Test filtering by author/date
   - Test searching by title

### 5.3 Run Tests (Optional)

```bash
# Run Django tests
python manage.py test portfolio

# With verbose output
python manage.py test portfolio -v 2
```

---

## Deployment to Production

### 6.1 Pre-Deployment Checklist

- [ ] All migrations applied locally
- [ ] Database backed up
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] Debug mode disabled
- [ ] ALLOWED_HOSTS configured
- [ ] CSRF settings verified
- [ ] Database credentials in environment variables
- [ ] SSL/HTTPS enabled

### 6.2 Deploy to Hostinger VPS

1. **Connect to VPS:**
   ```bash
   ssh -i your_key.pem -l root your_vps_ip
   ```

2. **Pull Latest Code:**
   ```bash
   cd /home/django_user/abid_portfolio
   git pull origin main
   ```

3. **Install Dependencies:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Collect Static Files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Restart Services:**
   ```bash
   sudo systemctl restart gunicorn
   sudo systemctl restart nginx
   ```

7. **Verify Deployment:**
   ```bash
   # Check Gunicorn status
   sudo systemctl status gunicorn
   # Check Nginx status
   sudo systemctl status nginx
   ```

### 6.3 Create Superuser on Production

```bash
# SSH into your VPS
ssh -i your_key.pem -l django_user your_vps_ip

# Activate virtual environment
cd abid_portfolio
source venv/bin/activate

# Create superuser
python manage.py createsuperuser

# Follow prompts to create admin account
```

### 6.4 Access Production Admin

```
https://portfolio.abidnexus.com/admin/
```

Login with your production superuser credentials.

---

## Troubleshooting

### T.1 "No such table: portfolio_blog" Error

**Cause:** Migrations haven't been applied

**Solution:**
```bash
python manage.py migrate portfolio
python manage.py migrate
```

### T.2 "Author" Field Shows as Required in Old Migration

**Cause:** Using an old migration file

**Solution:**
```bash
# Delete migration 0004_blog_author_updated_at.py if it exists
# Ensure you're using the correct version with null=True, blank=True
python manage.py migrate portfolio
```

### T.3 Images Not Displaying

**Cause:** Static/media files not configured or collected

**Solution:**
```bash
# For development
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Add to urls.py:
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# For production, collect static files
python manage.py collectstatic --noinput
```

### T.4 Admin Login Not Working

**Cause:** Superuser not created or credentials incorrect

**Solution:**
```bash
# Create new superuser
python manage.py createsuperuser

# Or reset password for existing user
python manage.py changepassword admin
```

### T.5 Blog Not Showing on Website

**Cause:** Blog posts not marked as published

**Solution:**
1. Go to admin: `/admin/`
2. Edit the blog post
3. Set "Published Date" to current date or earlier
4. Click Save

### T.6 Author Field Empty

**Cause:** Blog created before author field added

**Solution:**
1. Go to admin: `/admin/`
2. Edit blog post
3. Select an author from dropdown
4. Click Save

---

## Blog Model Reference

### Fields:

```python
class Blog(models.Model):
    title = CharField(max_length=255)           # Blog title
    slug = SlugField(max_length=255, unique=True) # URL slug
    author = ForeignKey(User)                   # Author (linked to User)
    excerpt = TextField(blank=True)             # Short summary
    content = TextField()                       # Full content (HTML supported)
    published_date = DateField(null=True)       # Publication date
    created_at = DateTimeField(auto_now_add=True) # Creation timestamp
    updated_at = DateTimeField(auto_now=True)   # Last update timestamp
    image = ImageField(blank=True)              # Featured image
```

### URLs:

| URL | View | Purpose |
|-----|------|---------|
| `/blogs/` | `blogs` | List all blog posts |
| `/blogs/<slug>/` | `blog_detail` | Display single blog post |
| `/admin/` | Admin | Manage blog posts |

### Admin Features:

- **Filter:** By author, publication date, creation date
- **Search:** By title, excerpt, content, author username
- **Bulk Actions:** Delete selected posts
- **Prepopulated Fields:** Slug auto-generates from title

---

## Quick Reference Commands

```bash
# Run migrations
python manage.py migrate portfolio

# Create superuser
python manage.py createsuperuser

# Change superuser password
python manage.py changepassword admin

# Start development server
python manage.py runserver

# Open shell
python manage.py shell

# View all users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()

# Check admin panel
# http://localhost:8000/admin/

# View blog list
# http://localhost:8000/blogs/
```

---

## Support & Documentation

- **Django Official Docs:** https://docs.djangoproject.com/
- **Django Models:** https://docs.djangoproject.com/en/stable/topics/db/models/
- **Django Admin:** https://docs.djangoproject.com/en/stable/ref/contrib/admin/
- **Pillow (Image Handling):** https://pillow.readthedocs.io/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-02-08 | Initial blog setup with author field support |

---

## License

This guide is part of the Abid Portfolio project. Follow your project's license terms for usage and distribution.

---

**Last Updated:** February 8, 2024
