# Blog System - Quick Reference Card

## ⚡ Essential Commands

### Database Setup
```bash
# Apply all migrations
python manage.py migrate portfolio

# Create admin account
python manage.py createsuperuser

# Change admin password
python manage.py changepassword admin
```

### Development
```bash
# Start development server
python manage.py runserver

# Open Django shell
python manage.py shell

# Check migrations status
python manage.py showmigrations
```

### Admin Tasks
```bash
# List all users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
>>> exit()

# Delete user
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(username='username').delete()
>>> exit()
```

---

## 🌐 Essential URLs

| Purpose | URL |
|---------|-----|
| **Admin Panel** | `http://localhost:8000/admin/` |
| **Blog List** | `http://localhost:8000/blogs/` |
| **Blog Detail** | `http://localhost:8000/blogs/{slug}/` |
| **Home** | `http://localhost:8000/` |

---

## 👨‍💻 Admin Panel Quick Guide

### Create Blog Post
1. Visit `http://localhost:8000/admin/`
2. Click "Blogs" → "+ Add Blog"
3. Fill in:
   - **Title**: Blog title
   - **Author**: Select from dropdown
   - **Content**: Full HTML content
   - **Image**: Optional featured image
   - **Published Date**: Leave blank for draft, date for publish
4. Click "Save"

### Edit Blog Post
1. Visit `http://localhost:8000/admin/`
2. Click "Blogs" → Click blog title
3. Modify fields
4. Click "Save"

### Delete Blog Post
1. Visit `http://localhost:8000/admin/`
2. Click checkbox next to blog title
3. Select "Delete selected blogs"
4. Confirm

---

## 📊 Model Fields Reference

```python
# Blog Model Fields
title           # Text (max 255 chars) - REQUIRED
slug            # URL slug (auto-generated) - REQUIRED
author          # User dropdown - OPTIONAL
excerpt         # Long text - OPTIONAL
content         # Long text (HTML) - REQUIRED
image           # Image upload - OPTIONAL
published_date  # Calendar date - OPTIONAL
created_at      # Auto timestamp - READ-ONLY
updated_at      # Auto timestamp - READ-ONLY
```

---

## 🔐 Admin Filter & Search

### Filter Blogs By:
- **Author** - Select from dropdown
- **Published Date** - Calendar widget
- **Created Date** - Calendar widget

### Search Blogs By:
- Title
- Excerpt
- Content
- Author username

---

## 📱 Blog Display Logic

### Published Blog (shows on website)
- `published_date` is set to today or earlier
- Shows in `/blogs/` list
- Shows author name
- Shows publication date

### Draft Blog (hidden from website)
- `published_date` is NULL or in future
- Does NOT show in `/blogs/` list
- Only admin can see in admin panel

---

## 🚀 One-Line Setup

```bash
# Complete setup in one command
python manage.py migrate portfolio && python manage.py createsuperuser && python manage.py runserver
```

---

## 🎨 Template Variables

### In `blogs.html` (Blog List)
```html
{% for post in posts %}
  {{ post.title }}           # Blog title
  {{ post.author.username }}  # Author username
  {{ post.author.get_full_name }}  # Author full name
  {{ post.published_date|date:"F d, Y" }}  # Formatted date
  {{ post.excerpt }}         # Short summary
  {{ post.image.url }}       # Image URL
  {% url 'portfolio:blog_detail' post.slug %}  # Blog URL
{% endfor %}
```

### In `blog_detail.html` (Single Blog)
```html
{{ post.title }}              # Blog title
{{ post.author.username }}    # Author username
{{ post.author.get_full_name }}  # Author full name
{{ post.published_date|date:"F d, Y" }}  # Formatted date
{{ post.content|safe }}       # Full content (HTML)
{{ post.image.url }}          # Image URL
```

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Blog not showing | Set `published_date` to today or earlier |
| Can't login to admin | Run `python manage.py createsuperuser` |
| Author dropdown empty | Create superuser first |
| Database errors | Run `python manage.py migrate portfolio` |
| Images not showing | Check media folder permissions |
| Slug errors | Publisher auto-generates from title |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `portfolio/models.py` | Blog model definition |
| `portfolio/admin.py` | Admin interface config |
| `portfolio/views.py` | Blog view logic |
| `portfolio/urls.py` | URL routing |
| `portfolio/templates/portfolio/blogs.html` | Blog list template |
| `portfolio/templates/portfolio/blog_detail.html` | Blog detail template |
| `portfolio/migrations/` | Database changes |

---

## ✅ Deployment Checklist

- [ ] Run: `python manage.py migrate portfolio`
- [ ] Run: `python manage.py createsuperuser` (on production)
- [ ] Test: `http://localhost:8000/admin/`
- [ ] Test: `http://localhost:8000/blogs/`
- [ ] Update `ALLOWED_HOSTS` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Deploy code to VPS
- [ ] Run migrations on VPS
- [ ] Verify `/admin/` works
- [ ] Verify `/blogs/` works

---

## 💡 Pro Tips

1. **Auto-slug Generation**: Slug auto-generates from title, edit if needed
2. **Draft vs Publish**: Leave `published_date` blank for drafts
3. **HTML Content**: You can use HTML tags in content field
4. **Author Required**: Set author when creating blog for better tracking
5. **Backup Database**: Before major updates, backup `db.sqlite3`

---

## 📞 Need Help?

Refer to:
- `IMPLEMENTATION_SUMMARY.md` - Overview of all changes
- `BLOG_SETUP_AND_DEPLOYMENT.md` - Detailed setup & deployment guide
- Django Docs: https://docs.djangoproject.com/

---

**Last Updated:** February 8, 2024
**Version:** 1.0
