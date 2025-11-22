"""
Generate professional project placeholder images using PIL.
Run: python manage.py generate_project_images
"""
import os
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Generate professional placeholder images for projects'

    def handle(self, *args, **options):
        # Create media/projects directory if it doesn't exist
        project_images_dir = Path(settings.MEDIA_ROOT) / 'projects'
        project_images_dir.mkdir(parents=True, exist_ok=True)

        # Define projects with their colors and icons
        projects = [
            {
                'filename': 'django-ml.png',
                'title': 'Django ML',
                'bg_color': '#092E20',
                'icon': '🎯',
            },
            {
                'filename': 'data-viz.png',
                'title': 'Data Viz',
                'bg_color': '#1f77b4',
                'icon': '📊',
            },
            {
                'filename': 'rag-qa.png',
                'title': 'RAG Q&A',
                'bg_color': '#667eea',
                'icon': '🧠',
            },
            {
                'filename': 'local-ai.png',
                'title': 'Local AI',
                'bg_color': '#43e97b',
                'icon': '💬',
            },
            {
                'filename': 'hugging-face.png',
                'title': 'HF Hub',
                'bg_color': '#FFD21E',
                'icon': '🤗',
            },
            {
                'filename': 'lora-tuning.png',
                'title': 'LoRA',
                'bg_color': '#00d4ff',
                'icon': '🔧',
            },
        ]

        for project in projects:
            # Create image
            img = Image.new('RGB', (800, 450), color=project['bg_color'])
            draw = ImageDraw.Draw(img)

            # Try to use a nice font; fallback to default if not available
            try:
                title_font = ImageFont.truetype("arial.ttf", 80)
                icon_font = ImageFont.truetype("arial.ttf", 120)
            except OSError:
                title_font = ImageFont.load_default()
                icon_font = ImageFont.load_default()

            # Draw icon (emoji or text)
            icon_bbox = draw.textbbox((0, 0), project['icon'], font=icon_font)
            icon_width = icon_bbox[2] - icon_bbox[0]
            icon_height = icon_bbox[3] - icon_bbox[1]
            icon_x = (800 - icon_width) // 2
            icon_y = (450 - icon_height) // 2 - 40
            draw.text((icon_x, icon_y), project['icon'], fill='white', font=icon_font)

            # Draw title
            title_bbox = draw.textbbox((0, 0), project['title'], font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (800 - title_width) // 2
            title_y = icon_y + icon_height + 20
            draw.text((title_x, title_y), project['title'], fill='white', font=title_font)

            # Save image
            filepath = project_images_dir / project['filename']
            img.save(filepath, 'PNG')
            self.stdout.write(self.style.SUCCESS(f'Created: {filepath}'))

        self.stdout.write(self.style.SUCCESS('All project images generated successfully!'))
