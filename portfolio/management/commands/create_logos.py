"""
Create professional project logos and brand logo for the portfolio.
Run: python manage.py create_logos
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Create professional project logos and brand logo'

    def create_abid_logo(self):
        """Create the main Abid Hussain brand logo with professional blue and gold"""
        # Professional gradient: navy blue to teal
        img = Image.new('RGB', (400, 200), color='#1a365d')
        draw = ImageDraw.Draw(img)

        # Draw elegant gradient background (navy to teal)
        for i in range(0, 400, 10):
            # Navy blue (26, 54, 93) to Teal (0, 102, 102)
            r = int(26 + (i / 400) * (-26))
            g = int(54 + (i / 400) * 48)
            b = int(93 + (i / 400) * 9)
            draw.rectangle([(i, 0), (i + 10, 200)], fill=(r, g, b))

        try:
            title_font = ImageFont.truetype("arial.ttf", 52)
            subtitle_font = ImageFont.truetype("arial.ttf", 20)
        except OSError:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Draw "Abid" text in white
        draw.text((40, 25), "Abid", fill='#ffffff', font=title_font)
        # Draw "Hussain" text in gold
        draw.text((40, 85), "Hussain", fill='#ffc107', font=title_font)
        # Draw subtitle in light silver
        draw.text((40, 155), "AI & Data Science Specialist", fill='#d4d4d8', font=subtitle_font)

        return img

    def create_project_logos(self):
        """Create professional logos for each project"""
        logos = {
            'django-ml.png': {
                'bg': '#092E20',  # Django green
                'icon': '🎯',
                'title': 'Django ML',
                'subtitle': 'Production APIs'
            },
            'data-viz.png': {
                'bg': '#1f77b4',  # Plotly blue
                'icon': '📊',
                'title': 'Data Viz',
                'subtitle': 'Interactive Dashboards'
            },
            'rag-qa.png': {
                'bg': '#667eea',  # Purple
                'icon': '🧠',
                'title': 'RAG Q&A',
                'subtitle': 'Semantic Search'
            },
            'local-ai.png': {
                'bg': '#43e97b',  # Green
                'icon': '💬',
                'title': 'Local AI',
                'subtitle': 'Offline LLMs'
            },
            'hugging-face.png': {
                'bg': '#FFD21E',  # HF yellow
                'icon': '🤗',
                'title': 'Hugging Face',
                'subtitle': 'Model Hub'
            },
            'lora-tuning.png': {
                'bg': '#00d4ff',  # Cyan
                'icon': '🔧',
                'title': 'LoRA Tuning',
                'subtitle': 'Fine-tuning'
            },
        }

        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            subtitle_font = ImageFont.truetype("arial.ttf", 28)
        except OSError:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        project_logos_dir = Path(settings.MEDIA_ROOT) / 'projects' / 'logos'
        project_logos_dir.mkdir(parents=True, exist_ok=True)

        for filename, config in logos.items():
            img = Image.new('RGB', (400, 300), color=config['bg'])
            draw = ImageDraw.Draw(img)

            # Draw icon
            icon_bbox = draw.textbbox((0, 0), config['icon'], font=title_font)
            icon_w = icon_bbox[2] - icon_bbox[0]
            icon_h = icon_bbox[3] - icon_bbox[1]
            draw.text(((400 - icon_w) // 2, 40), config['icon'], fill='white', font=title_font)

            # Draw title
            title_bbox = draw.textbbox((0, 0), config['title'], font=subtitle_font)
            title_w = title_bbox[2] - title_bbox[0]
            draw.text(((400 - title_w) // 2, 150), config['title'], fill='white', font=subtitle_font)

            # Draw subtitle
            subtitle_bbox = draw.textbbox((0, 0), config['subtitle'], font=subtitle_font)
            subtitle_w = subtitle_bbox[2] - subtitle_bbox[0]
            draw.text(((400 - subtitle_w) // 2, 210), config['subtitle'], fill='#cccccc', font=subtitle_font)

            filepath = project_logos_dir / filename
            img.save(filepath, 'PNG')
            self.stdout.write(self.style.SUCCESS(f'Created: {filepath}'))

        return project_logos_dir

    def handle(self, *args, **options):
        media_dir = Path(settings.MEDIA_ROOT)
        media_dir.mkdir(parents=True, exist_ok=True)

        # Create Abid Hussain logo
        self.stdout.write('Creating Abid Hussain brand logo...')
        abid_logo = self.create_abid_logo()
        abid_logo_path = media_dir / 'abid_hussain_logo.png'
        abid_logo.save(abid_logo_path, 'PNG')
        self.stdout.write(self.style.SUCCESS(f'✅ Brand logo created: {abid_logo_path}'))

        # Create project logos
        self.stdout.write('\nCreating project-specific logos...')
        self.create_project_logos()

        self.stdout.write(self.style.SUCCESS('\n✅ All logos created successfully!'))
