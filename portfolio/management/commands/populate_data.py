import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from portfolio.models import Profile, SkillCategory, Skill, Education, Project, Service

class Command(BaseCommand):
    help = 'Populate database with CV data'

    def handle(self, *args, **options):
        # Load CV data
        cv_data = {
            "name": "ABID HUSSAIN",
            "contact": {
                "phone": "0301-4850613",
                "email": "abidhussainnoul512@gmail.com",
                "address": "Lahore, Punjab, Pakistan"
            },
            "objective": "To apply my expertise in Python, Django (Web Development), and data science workflows alongside advanced skills in AI and Generative Models (LLMs, LoRA/QLoRA, RAG/CAG, NLP, AI agents, and prompt engineering) to build intelligent, data-driven solutions. I aim to leverage my experience in data analysis, visualization (Power BI, Tableau, Plotly), cloud (AWS), and automation tools (n8n, data scraping) to solve real-world problems, enhance decision-making, and drive innovation in a forward-looking organization.",
            "profile": {
                "father_name": "Hadayat Ali",
                "date_of_birth": "Feb, 15, 1986.",
                "nationality": "Pakistani",
                "cnic": "35401-1249389-9",
                "marital_status": "Married",
                "domicile": "Lahore (Punjab)",
                "religion": "Islam",
                "height": "5 fit, 10 Inch."
            },
            "skills": {
                "programming_languages": ["Python", "Markdown", "Html", "CSS"],
                "frameworks_libraries": ["Django (Web Development)", "Pandas", "NumPy", "Scikit-learn", "Matplotlib", "Seaborn", "Plotly", "Altair", "PyTorch", "Vibe Coding"],
                "artificial_intelligence": ["Generative AI", "LLMs(LoRA/QLoRA)", "NLP", "Prompt Engineering", "AI Agents", "RAG & CAG", "and Offline RAG-based Q&A Applications"],
                "automation_workflows": ["n8n", "Data Scraping", "API Integration"],
                "data_analysis_visualization": ["Power BI", "Tableau", "Excel", "PowerPoint"],
                "cloud_databases": ["AWS", "MySQL", "Hostinger kvme"],
                "software_tools": ["CorelDraw", "Adobe Photoshop", "Adobe Flash"],
                "platforms": ["Visual Studio Code", "Jupyter Notebook", "PyCharm"]
            },
            "social_skills": ["Communication Skills", "Analytical Skills", "Attention to Detail", "Negotiation Skills", "Interpersonal Skills", "Leadership"],
            "education": [
                "Advanced techniques in machine learning (ML) & Deep learning (DL) & Artificial intelligence (AI) and Django in 2025 from Codanics.com",
                "Data Science in 2024 from Codanics.com",
                "Master in Economics, Passing Year 2012, Awarded by Punjab University."
            ]
        }

        # Clear existing data
        Profile.objects.all().delete()
        SkillCategory.objects.all().delete()
        Education.objects.all().delete()
        Project.objects.all().delete()
        Service.objects.all().delete()

        # Create Profile
        profile = Profile.objects.create(
            name=cv_data["name"],
            email=cv_data["contact"]["email"],
            phone=cv_data["contact"]["phone"],
            address=cv_data["contact"]["address"],
            objective=cv_data["objective"],
            father_name=cv_data["profile"]["father_name"],
            date_of_birth=cv_data["profile"]["date_of_birth"],
            cnic=cv_data["profile"]["cnic"],
            marital_status=cv_data["profile"]["marital_status"],
            domicile=cv_data["profile"]["domicile"],
            religion=cv_data["profile"]["religion"],
            height=cv_data["profile"]["height"]
        )
        self.stdout.write(f'Created profile: {profile.name}')

        # Create Skill Categories and Skills
        skill_categories = {
            'Programming Languages': {'skills': cv_data["skills"]["programming_languages"], 'icon': 'fas fa-code'},
            'Frameworks & Libraries': {'skills': cv_data["skills"]["frameworks_libraries"], 'icon': 'fas fa-layer-group'},
            'Artificial Intelligence': {'skills': cv_data["skills"]["artificial_intelligence"], 'icon': 'fas fa-brain'},
            'Automation & Workflows': {'skills': cv_data["skills"]["automation_workflows"], 'icon': 'fas fa-cogs'},
            'Data Analysis & Visualization': {'skills': cv_data["skills"]["data_analysis_visualization"], 'icon': 'fas fa-chart-bar'},
            'Cloud & Databases': {'skills': cv_data["skills"]["cloud_databases"], 'icon': 'fas fa-cloud'},
            'Software Tools': {'skills': cv_data["skills"]["software_tools"], 'icon': 'fas fa-tools'},
            'Platforms': {'skills': cv_data["skills"]["platforms"], 'icon': 'fas fa-desktop'},
            'Social Skills': {'skills': cv_data["social_skills"], 'icon': 'fas fa-users'}
        }

        for category_name, category_data in skill_categories.items():
            category = SkillCategory.objects.create(
                name=category_name,
                icon=category_data['icon']
            )
            
            for skill_name in category_data['skills']:
                proficiency = 85 if category_name == 'Programming Languages' else 80
                if category_name == 'Artificial Intelligence':
                    proficiency = 90
                elif category_name == 'Frameworks & Libraries':
                    proficiency = 88
                
                Skill.objects.create(
                    category=category,
                    name=skill_name,
                    proficiency=proficiency
                )
            
            self.stdout.write(f'Created skill category: {category_name} with {len(category_data["skills"])} skills')

        # Create Education
        education_data = [
            {
                'degree': 'Advanced ML/DL/AI and Django',
                'institution': 'Codanics.com',
                'year': '2025',
                'description': 'Advanced techniques in machine learning (ML) & Deep learning (DL) & Artificial intelligence (AI) and Django'
            },
            {
                'degree': 'Data Science Certification',
                'institution': 'Codanics.com',
                'year': '2024',
                'description': 'Comprehensive Data Science program'
            },
            {
                'degree': 'Master in Economics',
                'institution': 'Punjab University',
                'year': '2012',
                'description': 'Master\'s degree in Economics'
            }
        ]

        for edu in education_data:
            Education.objects.create(**edu)
            self.stdout.write(f'Created education: {edu["degree"]}')

        # Create Sample Projects (with correct GitHub URLs and professional descriptions)
        projects_data = [
            {
                'title': 'Django Tip Prediction ML App',
                'description': 'Production-grade ML API built with Django for tip prediction. Features model versioning, REST API endpoints, Docker containerization, and scalable inference pipelines for real-world ML deployment.',
                'technologies': 'Django, DRF, Scikit-learn, PostgreSQL, Docker, REST APIs',
                'github_url': 'https://github.com/abid4850/tip_prediction_django_app',
                'live_url': '',
                'featured': True,
                'image_file': 'django-ml.png',
            },
            {
                'title': 'Interactive Data Visualization Dashboard',
                'description': 'Advanced interactive dashboards with drill-down analytics, KPIs, real-time data feeds and exportable reports. Built with Plotly, Streamlit, and optimized Pandas pipelines for high-performance analytics and insights.',
                'technologies': 'Plotly, Streamlit, Pandas, SQL, JavaScript, Data Analysis',
                'github_url': 'https://github.com/abid4850/WordCloud_App',
                'live_url': '',
                'featured': True,
                'image_file': 'data-viz.png',
            },
            {
                'title': 'RAG Question-Answering App',
                'description': 'Retrieval-Augmented Generation (RAG) system for semantic search over PDFs and documents. Uses FAISS vector embeddings, LLM-powered answering, document parsing, and web UI for intelligent Q&A on custom documents.',
                'technologies': 'Python, FAISS, Vector Embeddings, LLMs, NLP, Streamlit, RAG',
                'github_url': 'https://github.com/abid4850/Universal-RAG-Q-A-App',
                'live_url': '',
                'featured': True,
                'image_file': 'rag-qa.png',
            },
            {
                'title': 'Local AI Chatbot (Ollama)',
                'description': 'Offline-first AI chatbot powered by local LLM models via Ollama. Features conversational memory, embedding-based retrieval, secure processing and low-latency inference without cloud dependencies.',
                'technologies': 'Ollama, Local LLMs, Python, Embeddings, Conversational AI',
                'github_url': 'https://github.com/abid4850/Universal-RAG-Q-A-App',
                'live_url': '',
                'featured': False,
                'image_file': 'local-ai.png',
            },
            {
                'title': 'Hugging Face Model Hub Integration',
                'description': 'Curated Hugging Face Model Hub featuring fine-tuned transformers, custom datasets, and inference API wrappers. Demonstrates model versioning, evaluation metrics, and production deployment on HF Hub.',
                'technologies': 'Hugging Face, Transformers, PyTorch, NLP, Model Hub, MLOps',
                'github_url': 'https://github.com/abid4850/DSAAMP-Data-Science-to-Ai-Agent-mentorship-programme-/tree/main/07_NLP',
                'live_url': 'https://huggingface.co/Abidhussain12',
                'featured': True,
                'image_file': 'hugging-face.png',
            },
            {
                'title': 'LoRA Fine-Tuning for LLMs',
                'description': 'Efficient LoRA-based fine-tuning framework for large language models. Includes training scripts, evaluation pipelines, hyperparameter optimization, and Hugging Face deployment examples for production LLM customization.',
                'technologies': 'LoRA, Transformers, PyTorch, Hugging Face, Fine-tuning, QLoRA',
                'github_url': 'https://huggingface.co/Abidhussain12',
                'live_url': 'https://huggingface.co/Abidhussain12',
                'featured': False,
                'image_file': 'lora-tuning.png',
            },
        ]

        projects_dir = Path(settings.MEDIA_ROOT) / 'projects'
        for project_data in projects_data:
            image_file = project_data.pop('image_file', None)
            project = Project.objects.create(**project_data)
            
            # Attach image if it exists
            if image_file and projects_dir.exists():
                image_path = projects_dir / image_file
                if image_path.exists():
                    with open(image_path, 'rb') as f:
                        project.image.save(image_file, File(f), save=True)
                    self.stdout.write(f'  ↳ Image attached: {image_file}')
            
            self.stdout.write(f'Created project: {project.title}')

        # Create Services
        services_data = [
            {
                'title': 'Web Development',
                'description': 'Professional Django web development services for scalable and robust web applications.',
                'icon': 'fas fa-globe'
            },
            {
                'title': 'Data Science & Analytics',
                'description': 'Advanced data analysis, visualization, and machine learning solutions for business insights.',
                'icon': 'fas fa-chart-line'
            },
            {
                'title': 'AI & Machine Learning',
                'description': 'Custom AI solutions including NLP, computer vision, and predictive modeling.',
                'icon': 'fas fa-robot'
            },
            {
                'title': 'Automation & Workflows',
                'description': 'Process automation and workflow optimization using modern tools and technologies.',
                'icon': 'fas fa-sync-alt'
            }
        ]

        for service in services_data:
            Service.objects.create(**service)
            self.stdout.write(f'Created service: {service["title"]}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with CV data!'))

