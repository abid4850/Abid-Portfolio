"""
Script to attach professional images to blog posts
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abid_portfolio.settings')
sys.path.insert(0, r'C:\Users\abidh\OneDrive\Desktop\abid_portfolio')
django.setup()

from portfolio.models import Blog
from pathlib import Path
from django.core.files import File

media_dir = Path(r'C:\Users\abidh\OneDrive\Desktop\abid_portfolio\media\blog')

# Get blog posts
try:
    blog1 = Blog.objects.get(slug='ai-and-its-features-in-detail')
    blog2 = Blog.objects.get(slug='humans-and-ai-building-a-collaborative-future')
    
    # Attach images
    ai_image_path = media_dir / 'ai-blog-header.png'
    if ai_image_path.exists():
        with open(ai_image_path, 'rb') as f:
            blog1.image.save('ai-blog-header.png', File(f), save=True)
        print(f'✅ Attached image to: {blog1.title}')
    
    human_ai_image_path = media_dir / 'human-ai-blog-header.png'
    if human_ai_image_path.exists():
        with open(human_ai_image_path, 'rb') as f:
            blog2.image.save('human-ai-blog-header.png', File(f), save=True)
        print(f'✅ Attached image to: {blog2.title}')
    
    print('\n✨ Blog images are properly attached!')
    
except Blog.DoesNotExist as e:
    print(f'Error: Blog post not found - {e}')
except Exception as e:
    print(f'Error: {e}')
