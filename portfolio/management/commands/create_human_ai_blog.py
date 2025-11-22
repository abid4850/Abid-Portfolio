"""
Create a professional 'Human and AI' blog post with header image.
Run: python manage.py create_human_ai_blog
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
    help = 'Create a professional "Human and AI" blog post with header image'

    def create_human_ai_blog_image(self):
        """Create a professional Human and AI blog header image"""
        img = Image.new('RGB', (1400, 700), color='white')
        
        # Draw gradient background (purple to indigo to blue)
        draw = ImageDraw.Draw(img)
        for x in range(1400):
            ratio = x / 1400
            r = int(102 * (1 - ratio) + 59 * ratio)
            g = int(51 * (1 - ratio) + 130 * ratio)
            b = int(153 * (1 - ratio) + 246 * ratio)
            draw.line([(x, 0), (x, 700)], fill=(r, g, b))

        # Draw semi-transparent overlay for text contrast
        overlay = Image.new('RGBA', (1400, 700), (0, 0, 0, 50))
        img.paste(overlay, (0, 0), overlay)

        try:
            title_font = ImageFont.truetype("arial.ttf", 96)
            subtitle_font = ImageFont.truetype("arial.ttf", 48)
        except OSError:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Draw human and AI icons
        draw.text((80, 220), "👤", fill='white', font=ImageFont.truetype("arial.ttf", 160) if 'arial.ttf' else ImageFont.load_default())
        draw.text((250, 220), "🤖", fill='white', font=ImageFont.truetype("arial.ttf", 160) if 'arial.ttf' else ImageFont.load_default())

        # Draw title
        title = "Humans and AI"
        draw.text((480, 150), title, fill='white', font=title_font)

        # Draw subtitle
        subtitle = "Building a Collaborative Future"
        draw.text((480, 300), subtitle, fill='#e0f2fe', font=subtitle_font)

        # Draw description
        desc_font = ImageFont.truetype("arial.ttf", 28) if 'arial.ttf' else ImageFont.load_default()
        description = "Understanding Human-AI Collaboration, Opportunities & Challenges"
        draw.text((100, 550), description, fill='#cbd5e1', font=desc_font)

        return img

    def handle(self, *args, **options):
        # Check if blog post already exists
        slug = slugify("Humans and AI: Building a Collaborative Future")
        if Blog.objects.filter(slug=slug).exists():
            self.stdout.write(self.style.WARNING(f"Blog post '{slug}' already exists. Skipping."))
            return

        # Create image
        self.stdout.write('Generating Human and AI blog header image...')
        img = self.create_human_ai_blog_image()
        
        # Save to BytesIO
        bio = BytesIO()
        img.save(bio, format='PNG', optimize=True)
        bio.seek(0)

        # Blog content - Professional, detailed, human-written style
        blog_title = "Humans and AI: Building a Collaborative Future"
        blog_excerpt = "Explore how humans and artificial intelligence are reshaping the future together. Discover the symbiosis between human creativity and AI capabilities, and understand how this partnership is transforming industries, society, and the nature of work itself."
        
        blog_content = """<h2>🌍 The Human-AI Partnership: A New Era</h2>
<p>We stand at a remarkable crossroads in human history. For the first time, we have created tools that can learn, adapt, and perform cognitive tasks that were once exclusively human domains. Yet despite this technological marvel, the most powerful breakthroughs are not happening when AI works alone—they occur when humans and artificial intelligence collaborate.</p>
<p>This is not a story of replacement; it is a story of augmentation. It is about how human wisdom, creativity, and emotional intelligence combine with AI's computational power, speed, and data processing capabilities to create something far greater than either could achieve alone.</p>

<h2>💡 What Makes This Partnership Special?</h2>

<h3>The Strengths Humans Bring</h3>
<ul>
<li><strong>Creativity & Innovation:</strong> Humans possess imagination, the ability to think sideways, and to see connections where none existed before. We dream of futures that don't exist yet.</li>
<li><strong>Emotional Intelligence:</strong> We understand context, empathy, and nuance. We know when rules should be broken and why compassion matters.</li>
<li><strong>Ethical Judgment:</strong> Humans make moral decisions. We understand responsibility and can weigh competing values in complex situations.</li>
<li><strong>Adaptability:</strong> We learn from failure, adjust to unexpected change, and thrive in uncertain environments.</li>
<li><strong>Purpose & Meaning:</strong> We ask "why" a question that drives purpose and meaningful action.</li>
</ul>

<h3>The Strengths AI Brings</h3>
<ul>
<li><strong>Scale & Speed:</strong> AI processes vast amounts of data and performs calculations in seconds that would take humans lifetimes.</li>
<li><strong>Consistency:</strong> AI performs repetitive tasks without fatigue, maintaining accuracy across millions of operations.</li>
<li><strong>Pattern Recognition:</strong> Machine learning algorithms identify subtle patterns hidden in data that human eyes would never see.</li>
<li><strong>Objectivity (Relative):</strong> AI makes decisions based on data without personal bias though we must design it carefully to avoid hidden bias.</li>
<li><strong>24/7 Availability:</strong> AI doesn't sleep, doesn't get tired, and works at any hour to support human goals.</li>
</ul>

<h2>🚀 Real-World Examples of Human-AI Collaboration</h2>

<h3>Healthcare: Diagnosing Disease with Greater Accuracy</h3>
<p>In hospitals around the world, radiologists now work alongside AI systems that analyze medical images. The AI can scan thousands of X-rays and MRIs in minutes, flagging anomalies with superhuman accuracy. But it takes a human doctor to understand the patient's full medical history, ask the right questions, and make treatment decisions that consider quality of life, family wishes, and ethical dimensions that numbers alone cannot capture.</p>
<p>Result: Earlier detection, better outcomes, and doctors spending more time talking to patients instead of reviewing images.</p>

<h3>Scientific Discovery: Accelerating Research</h3>
<p>Researchers use AI to analyze massive datasets and run simulations that would take years to compute by hand. AlphaFold, for example, predicted the 3D structures of proteins a problem scientists had been trying to solve for 50 years. But it was human scientists who framed the problem, verified the results, and figured out how to apply this knowledge to develop new medicines.</p>
<p>Result: Scientific breakthroughs that improve lives, happening faster than ever before.</p>

<h3>Business: Making Better Decisions</h3>
<p>Companies use AI to analyze market trends, customer behavior, and operational data. The AI identifies what happened and predicts what might happen. But it takes human leadership to decide what should happen to choose which opportunities align with company values, which risks are worth taking, and how to build teams and culture.</p>
<p>Result: Data-driven decisions that are also wise, ethical, and strategically sound.</p>

<h3>Creative Industries: Enhancing Human Talent</h3>
<p>Musicians use AI to compose accompaniments. Designers use AI to generate variations on their concepts. Writers use AI to research and draft initial content. But the human artist makes the final creative choices deciding what moves the heart, what tells the story, what resonates with beauty and truth.</p>
<p>Result: Artists amplified, freed from tedious work, able to focus on what only humans can do: create meaning.</p>

<h2>⚡ The Challenges We Must Address</h2>

<h3>Privacy & Security</h3>
<p>AI systems require vast amounts of data to learn. But data is personal. We must build systems that respect privacy, ensure security, and give people control over their information. This requires both technical solutions and human wisdom about what trade-offs are acceptable.</p>

<h3>Bias & Fairness</h3>
<p>AI learns from historical data, and history carries the prejudices of the past. Without careful human oversight, AI can perpetuate or amplify discrimination. Humans must actively design AI systems to be fair, and continuously monitor and correct for bias.</p>

<h3>Job Displacement & Reskilling</h3>
<p>As AI automates certain tasks, workers need support in transitioning to new roles. This is not just a technical problem—it requires empathy, investment in education, and policies that protect human dignity and opportunity.</p>

<h3>Transparency & Accountability</h3>
<p>When an AI system makes a decision that affects someone's life approving a loan, recommending medical treatment, or determining criminal sentencing people deserve to understand why. This requires AI developers and organizations to build explainability and ensure humans remain accountable for outcomes.</p>

<h3>Control & Alignment</h3>
<p>As AI systems become more powerful, we must ensure they remain aligned with human values and remain under human control. This requires ongoing collaboration between computer scientists, ethicists, policymakers, and society.</p>

<h2>🎯 The Future: How to Build It Right</h2>

<h3>Invest in Human Skills</h3>
<p>As routine work becomes automated, the premium on uniquely human skills critical thinking, communication, leadership, emotional intelligence, creativity will only increase. Education systems must evolve to cultivate these capabilities.</p>

<h3>Design Responsible AI</h3>
<p>Companies and researchers must prioritize ethics and transparency in AI development. This means testing for bias, building explainability, respecting privacy, and designing systems to augment human capability rather than replace human judgment.</p>

<h3>Create New Kinds of Jobs</h3>
<p>History shows that technology creates new kinds of work we couldn't have imagined before. From smartphone developers to social media managers to AI trainers, new roles emerge. We must invest in infrastructure and education to help people transition to these new opportunities.</p>

<h3>Establish Strong Governance</h3>
<p>We need thoughtful regulation that protects people while allowing innovation. This requires dialogue between government, industry, academia, and society—a collective human effort to shape technology toward good.</p>

<h3>Stay Focused on Human Flourishing</h3>
<p>Technology should serve human purposes. The question is not "how powerful can AI become" but "how can AI help humans live better lives?" This requires us to regularly ask: Does this AI respect human dignity? Does it expand human capability? Does it help us build communities and meaning?</p>

<h2>🔮 The Optimistic Path Forward</h2>

<p>The relationship between humans and AI doesn't have to be adversarial. We are not in a race with machines; we are using machines to run a relay race toward a better future.</p>

<p>Imagine a world where:</p>
<ul>
<li>Doctors spend less time on administrative work and more time listening to patients</li>
<li>Scientists discover cures faster, freeing researchers to ask even bigger questions</li>
<li>Artists and creators are freed from tedious work and can focus on inspiration</li>
<li>Workers displaced by automation have access to education and support to transition to meaningful new careers</li>
<li>AI systems operate transparently, with clear accountability and human oversight</li>
<li>Technology amplifies human capability while respecting human agency and dignity</li>
</ul>

<p>This future is possible if we make deliberate choices right now.</p>

<h2>💬 Final Thoughts: The Choice Is Ours</h2>

<p>Artificial Intelligence is not destiny. It is a tool we are building, and we get to choose how it evolves. We can choose to build AI systems that respect privacy, ensure fairness, and serve human flourishing. We can choose to invest in human development and transition support. We can choose to maintain human agency and oversight in decisions that matter.</p>

<p>The partnership between humans and AI is not predetermined. It is something we must actively build—with intention, wisdom, and a commitment to human values.</p>

<p>The future belongs to those who can combine human creativity with computational power, human judgment with data-driven insight, human compassion with technological efficiency. The best use of artificial intelligence is not to replace humans. It is to make humans better at being human.</p>

<p>And that is a future worth building together.</p>

<h2>❓ Questions to Consider</h2>
<ul>
<li>How can you leverage AI in your own work while maintaining your unique human value?</li>
<li>What ethical considerations matter most to you in how AI is developed?</li>
<li>How can organizations better support workers transitioning in an AI-driven world?</li>
<li>What human skills do you think will matter most in an AI-augmented future?</li>
</ul>
"""

        # Create blog post
        django_file = File(bio, name='human-ai-blog-header.png')
        blog = Blog.objects.create(
            title=blog_title,
            slug=slug,
            excerpt=blog_excerpt,
            content=blog_content,
            published_date=date.today()
        )
        blog.image.save('human-ai-blog-header.png', django_file, save=True)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Blog post created: "{blog_title}"'))
        self.stdout.write(self.style.SUCCESS(f'✅ Header image attached: human-ai-blog-header.png'))
        self.stdout.write(self.style.SUCCESS('\n✨ Professional blog post is now live!'))
