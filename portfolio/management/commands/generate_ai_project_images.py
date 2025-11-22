"""
Generate professional AI-like images for projects and attach them to Project.image.
Run: python manage.py generate_ai_project_images [--force]

This command uses PIL to create gradient images with the project title and a subtitle
derived from the technologies. It does not require external APIs. If you want real AI
images from an external service (Midjourney, DALL·E, etc.) we can add integration
when you provide API keys.
"""
import hashlib
import os
from pathlib import Path
from io import BytesIO

from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from PIL import Image, ImageDraw, ImageFont

from portfolio.models import Project


def _slugify(name: str) -> str:
    # safe filename
    return "ai-" + "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


def _choose_gradient(title: str):
    # Choose two colors deterministically from title hash
    h = hashlib.md5(title.encode("utf-8")).hexdigest()
    # pick color pairs
    palettes = [
        ((26,54,93), (0,102,102)),  # navy -> teal
        ((50,100,200), (120,60,180)),  # blue -> purple
        ((34,197,94), (16,185,129)),  # green shades
        ((37,99,235), (99,102,241)),  # indigo
        ((255,159,67), (255,99,132)),  # warm orange-pink
    ]
    idx = int(h[:8], 16) % len(palettes)
    return palettes[idx]


def _draw_gradient(img: Image.Image, c1, c2):
    w, h = img.size
    draw = ImageDraw.Draw(img)
    for x in range(w):
        ratio = x / max(1, w - 1)
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(x, 0), (x, h)], fill=(r, g, b))


def _create_project_image(title: str, subtitle: str, size=(1200, 675)) -> Image.Image:
    img = Image.new("RGB", size, color=(255, 255, 255))
    c1, c2 = _choose_gradient(title)
    _draw_gradient(img, c1, c2)

    draw = ImageDraw.Draw(img)
    try:
        title_font = ImageFont.truetype("arial.ttf", 72)
        subtitle_font = ImageFont.truetype("arial.ttf", 36)
    except OSError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    w, h = img.size
    # draw translucent rectangle behind text for contrast
    rect_h = 180
    rect_w = int(w * 0.8)
    rect_x = (w - rect_w) // 2
    rect_y = int(h * 0.45) - rect_h // 2
    overlay = Image.new("RGBA", (rect_w, rect_h), (0, 0, 0, 80))
    img.paste(overlay, (rect_x, rect_y), overlay)

    # draw title centered
    title_w, title_h = draw.textsize(title, font=title_font)
    t_x = (w - title_w) // 2
    t_y = rect_y + 18
    draw.text((t_x, t_y), title, fill=(255, 255, 255), font=title_font)

    # subtitle
    sub_w, sub_h = draw.textsize(subtitle, font=subtitle_font)
    s_x = (w - sub_w) // 2
    s_y = t_y + title_h + 12
    draw.text((s_x, s_y), subtitle, fill=(230, 230, 230), font=subtitle_font)

    return img


class Command(BaseCommand):
    help = "Generate AI-like project images and attach to Project.image"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Regenerate images even if Project.image exists")

    def handle(self, *args, **options):
        media_dir = Path(settings.MEDIA_ROOT) / "projects"
        media_dir.mkdir(parents=True, exist_ok=True)

        force = options.get("force", False)
        projects = Project.objects.all()
        if not projects.exists():
            self.stdout.write(self.style.WARNING("No projects found."))
            return

        for project in projects:
            try:
                title = project.title or "Project"
                techs = ", ".join(getattr(project, "tech_list", []) or [])
                subtitle = techs if techs else (project.description[:120] if project.description else "")

                if project.image and not force:
                    self.stdout.write(self.style.NOTICE(f"Skipping (already has image): {project.title}"))
                    continue

                filename = _slugify(project.title) + ".png"
                filepath = media_dir / filename

                # Create image
                img = _create_project_image(title, subtitle)
                # Save to BytesIO
                bio = BytesIO()
                img.save(bio, format="PNG", optimize=True)
                bio.seek(0)

                # Attach to project.image
                django_file = File(bio, name=filename)
                project.image.save(filename, django_file, save=True)
                self.stdout.write(self.style.SUCCESS(f"Created and attached image for: {project.title} -> {filename}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed for {project.title}: {e}"))

        self.stdout.write(self.style.SUCCESS("\nAll project images processed."))
