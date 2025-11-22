"""
Create a professional AI blog post with header image.
Run: python manage.py create_ai_blog_post
"""
from datetime import date
from io import BytesIO
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify

from PIL import Image, ImageDraw, ImageFont

from portfolio.models import Blog


class Command(BaseCommand):
    help = 'Create a professional AI blog post with header image'

    def create_ai_blog_image(self):
        """Create a professional AI blog header image with gradient and text"""
        img = Image.new('RGB', (1400, 700), color='white')
        
        # Draw gradient background (navy to teal to cyan)
        draw = ImageDraw.Draw(img)
        for x in range(1400):
            ratio = x / 1400
            r = int(26 * (1 - ratio) + 0 * ratio)
            g = int(54 * (1 - ratio) + 150 * ratio)
            b = int(93 * (1 - ratio) + 200 * ratio)
            draw.line([(x, 0), (x, 700)], fill=(r, g, b))

        # Draw semi-transparent overlay for text contrast
        overlay = Image.new('RGBA', (1400, 700), (0, 0, 0, 40))
        img.paste(overlay, (0, 0), overlay)

        try:
            title_font = ImageFont.truetype("arial.ttf", 96)
            subtitle_font = ImageFont.truetype("arial.ttf", 48)
        except OSError:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Draw brain/AI icon representation
        draw.text((100, 250), "🧠", fill='white', font=ImageFont.truetype("arial.ttf", 200) if 'arial.ttf' else ImageFont.load_default())

        # Draw title
        title = "AI and Its Features"
        draw.text((450, 150), title, fill='white', font=title_font)

        # Draw subtitle
        subtitle = "In Comprehensive Detail"
        draw.text((450, 300), subtitle, fill='#e0f2fe', font=subtitle_font)

        # Draw description
        desc_font = ImageFont.truetype("arial.ttf", 28) if 'arial.ttf' else ImageFont.load_default()
        description = "Explore Machine Learning, Deep Learning, NLP, Computer Vision & More"
        draw.text((100, 550), description, fill='#cbd5e1', font=desc_font)

        return img

    def handle(self, *args, **options):
        # Check if blog post already exists
        slug = slugify("AI and Its Features in Detail")
        if Blog.objects.filter(slug=slug).exists():
            self.stdout.write(self.style.WARNING(f"Blog post '{slug}' already exists. Skipping."))
            return

        # Create image
        self.stdout.write('Generating AI blog header image...')
        img = self.create_ai_blog_image()
        
        # Save to BytesIO
        bio = BytesIO()
        img.save(bio, format='PNG', optimize=True)
        bio.seek(0)

        # Blog content
        blog_title = "AI and Its Features in Detail"
        blog_excerpt = "Explore the key features of Artificial Intelligence including Machine Learning, Deep Learning, Natural Language Processing, Computer Vision, Robotics, Expert Systems, and Predictive Analytics."
        
        blog_content = """<h2>🔍 What Is Artificial Intelligence (AI)?</h2>
<p>Artificial Intelligence refers to computer systems designed to perform tasks that traditionally require human intelligence. These tasks include learning from experience, understanding language, recognizing visual patterns, making decisions, and solving problems.</p>
<p>At its core, AI combines mathematics, data, algorithms, and computational power to simulate human-like intelligence — often performing certain tasks even better than humans.</p>

<h2>✨ Key Features of AI (Explained in Detail)</h2>

<h3>1. Machine Learning (ML)</h3>
<p>Machine Learning allows computers to learn automatically from data, without being manually programmed for every scenario.</p>
<p><strong>How ML works:</strong> ML algorithms study data patterns and use them to make predictions or decisions.</p>
<p><strong>Common examples:</strong></p>
<ul>
<li>Netflix recommending movies</li>
<li>Banks detecting fraud</li>
<li>Email providers filtering spam</li>
<li>Facebook identifying faces in photos</li>
</ul>

<h3>2. Deep Learning</h3>
<p>Deep Learning is an advanced type of machine learning inspired by the structure of the human brain.</p>
<p><strong>How it works:</strong> It uses neural networks with multiple layers to understand extremely complex patterns.</p>
<p><strong>Applications:</strong></p>
<ul>
<li>Self-driving cars analyzing road images</li>
<li>Virtual assistants like Siri & Google Assistant</li>
<li>Medical image diagnosis</li>
<li>AI image and voice generation</li>
</ul>

<h3>3. Natural Language Processing (NLP)</h3>
<p>NLP enables computers to interpret, understand, and generate human language.</p>
<p><strong>Real-world uses:</strong></p>
<ul>
<li>ChatGPT-like conversational systems</li>
<li>Google Translate</li>
<li>Sentiment detection in reviews</li>
<li>Automated emails and content generation</li>
</ul>

<h3>4. Computer Vision</h3>
<p>Computer Vision allows machines to "see" and analyze visual information.</p>
<p><strong>Examples:</strong></p>
<ul>
<li>Face unlock on smartphones</li>
<li>CCTV surveillance tracking</li>
<li>Product scanning in stores</li>
<li>Medical imaging (MRI, X-ray analysis)</li>
</ul>

<h3>5. Robotics & Automation</h3>
<p>Robotics powered by AI can perform tasks with accuracy, speed, and consistency often in hazardous environments.</p>
<p><strong>Applications:</strong></p>
<ul>
<li>Assembly line manufacturing</li>
<li>Autonomous drones</li>
<li>Warehouse robots</li>
<li>Robotic surgery tools</li>
</ul>

<h3>6. Expert Systems</h3>
<p>Expert systems mimic the decision-making of human experts within a specific domain.</p>
<p><strong>Examples:</strong></p>
<ul>
<li>Medical diagnosis tools</li>
<li>Investment advisory systems</li>
<li>Technical troubleshooting assistants</li>
</ul>

<h3>7. Predictive Analytics</h3>
<p>Predictive analytics uses AI to forecast future outcomes by analyzing historical data.</p>
<p><strong>Use cases:</strong></p>
<ul>
<li>Predicting stock market trends</li>
<li>Weather forecasting</li>
<li>Product demand planning</li>
<li>Identifying disease risks</li>
</ul>

<h2>🌍 The Impact of AI on Society</h2>
<p>Across every industry, AI is transforming the world by:</p>
<ul>
<li>Improving medical accuracy</li>
<li>Reducing business costs</li>
<li>Automating repetitive tasks</li>
<li>Enhancing personal digital experiences</li>
<li>Increasing workplace efficiency</li>
<li>Supporting education with personalized learning</li>
</ul>

<h2>🔮 The Future of AI</h2>
<p>The future of AI is incredibly promising, with innovations such as:</p>
<ul>
<li>Emotion-aware AI systems</li>
<li>Fully autonomous vehicles</li>
<li>AI-powered healthcare breakthroughs</li>
<li>Smart city automation</li>
<li>More natural human-machine communication</li>
</ul>

<h2>💡 Final Thoughts</h2>
<p>Artificial Intelligence is more than a technological advancement. it's a revolution. Understanding its features helps us see how deeply it influences our present and how critical it will be for our future.</p>
<p>From machine learning to robotics, AI is transforming industries, societies, and daily life. Whether you're a beginner, student, developer, or business owner, now is the perfect time to dive into the world of AI.</p>
"""

        # Create blog post
        django_file = File(bio, name='ai-blog-header.png')
        blog = Blog.objects.create(
            title=blog_title,
            slug=slug,
            excerpt=blog_excerpt,
            content=blog_content,
            published_date=date.today()
        )
        blog.image.save('ai-blog-header.png', django_file, save=True)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Blog post created: "{blog_title}"'))
        self.stdout.write(self.style.SUCCESS(f'✅ Header image attached: ai-blog-header.png'))
        self.stdout.write(self.style.SUCCESS('\n✨ Blog post is now live on your site!'))
