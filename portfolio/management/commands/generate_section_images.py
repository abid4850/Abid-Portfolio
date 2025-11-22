"""
Generate professional section images using PIL with gradients and icons.
Run: python manage.py generate_section_images
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Generate professional images for all page sections'

    def create_gradient_image(self, filename, title, subtitle, bg_gradient, icon, emoji=True):
        """Create a professional gradient image with text"""
        img = Image.new('RGB', (1200, 600), color='white')
        draw = ImageDraw.Draw(img)

        # Draw gradient background
        for i in range(0, 1200, 20):
            # Calculate gradient color
            ratio = i / 1200
            r = int(bg_gradient[0][0] * (1 - ratio) + bg_gradient[1][0] * ratio)
            g = int(bg_gradient[0][1] * (1 - ratio) + bg_gradient[1][1] * ratio)
            b = int(bg_gradient[0][2] * (1 - ratio) + bg_gradient[1][2] * ratio)
            draw.rectangle([(i, 0), (i + 20, 600)], fill=(r, g, b))


        try:
            title_font = ImageFont.truetype("arial.ttf", 80)
            subtitle_font = ImageFont.truetype("arial.ttf", 40)
            emoji_font = ImageFont.truetype("arial.ttf", 120)
        except OSError:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            emoji_font = ImageFont.load_default()

        # Draw emoji/icon
        draw.text((150, 180), icon, fill='white', font=emoji_font)

        # Draw title
        draw.text((400, 150), title, fill='white', font=title_font)

        # Draw subtitle
        draw.text((400, 280), subtitle, fill='white', font=subtitle_font)

        return img

    def handle(self, *args, **options):
        # Create sections directory
        sections_dir = Path(settings.MEDIA_ROOT) / 'sections'
        sections_dir.mkdir(parents=True, exist_ok=True)

        sections = [
            {
                'filename': 'hero-section.png',
                'title': 'AI & Data Science',
                'subtitle': 'Building Intelligent Solutions',
                'bg_gradient': ((30, 60, 120), (80, 130, 200)),  # Navy to Blue
                'icon': '🚀'
            },
            {
                'filename': 'about-section.png',
                'title': 'About Me',
                'subtitle': 'Python Developer | Data Scientist',
                'bg_gradient': ((45, 85, 150), (70, 120, 180)),  # Steel Blue
                'icon': '👨‍💻'
            },
            {
                'filename': 'skills-section.png',
                'title': 'Technical Skills',
                'subtitle': 'Expertise Across Full Stack',
                'bg_gradient': ((60, 100, 180), (100, 150, 220)),  # Medium Blue
                'icon': '🛠️'
            },
            {
                'filename': 'projects-section.png',
                'title': 'Featured Projects',
                'subtitle': 'Production-Ready Applications',
                'bg_gradient': ((40, 75, 145), (90, 140, 210)),  # Deep Blue
                'icon': '💼'
            },
            {
                'filename': 'services-section.png',
                'title': 'My Services',
                'subtitle': 'End-to-End Solutions',
                'bg_gradient': ((35, 70, 135), (85, 135, 200)),  # Ocean Blue
                'icon': '⚡'
            },
            {
                'filename': 'education-section.png',
                'title': 'Education',
                'subtitle': 'Continuous Learning',
                'bg_gradient': ((50, 90, 160), (100, 155, 225)),  # Sky Blue
                'icon': '🎓'
            },
            {
                'filename': 'contact-section.png',
                'title': 'Get In Touch',
                'subtitle': 'Let\'s Build Something Amazing',
                'bg_gradient': ((30, 65, 130), (80, 140, 210)),  # Dark Blue
                'icon': '📧'
            },
            {
                'filename': 'blog-section.png',
                'title': 'Insights & Articles',
                'subtitle': 'Technology & AI',
                'bg_gradient': ((40, 80, 150), (95, 150, 220)),  # Royal Blue
                'icon': '📝'
            },
        ]

        for section in sections:
            self.stdout.write(f'Creating {section["filename"]}...')
            img = self.create_gradient_image(
                section['filename'],
                section['title'],
                section['subtitle'],
                section['bg_gradient'],
                section['icon']
            )
            filepath = sections_dir / section['filename']
            img.save(filepath, 'PNG')
            self.stdout.write(self.style.SUCCESS(f'✅ Created: {filepath}'))

        self.stdout.write(self.style.SUCCESS('\n✨ All section images generated successfully!'))
