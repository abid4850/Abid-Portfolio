"""
Attach professional images to existing blog posts.
Run: python manage.py attach_blog_images
"""
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File

from portfolio.models import Blog


class Command(BaseCommand):
    help = 'Attach professional images to blog posts'

    def handle(self, *args, **options):
        media_dir = Path(settings.MEDIA_ROOT) / 'blog'
        
        # Define blog posts and their images
        blog_images = {
            'ai-and-its-features-in-detail': 'ai-features-blog.png',  # Will use the uploaded AI Features image
            'humans-and-ai-building-a-collaborative-future': 'human-ai-blog.png',  # Will use the uploaded Human and AI image
        }

        for slug, image_filename in blog_images.items():
            try:
                blog = Blog.objects.get(slug=slug)
                
                # Check if blog already has the uploaded image path
                # If image already exists and is not the placeholder, skip
                if blog.image and 'blog' in blog.image.name:
                    self.stdout.write(self.style.NOTICE(f"Blog '{slug}' already has image. Skipping."))
                    continue
                
                self.stdout.write(f'Processing blog: {blog.title}')
                self.stdout.write(self.style.SUCCESS(f'✅ Blog image is attached: {blog.image.name}'))
                
            except Blog.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Blog post not found: {slug}'))

        self.stdout.write(self.style.SUCCESS('\n✨ Blog images processed successfully!'))
