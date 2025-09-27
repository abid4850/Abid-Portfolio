import json
from django.core.management.base import BaseCommand
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
                "address": "ThathaNoulan, Sharaqpur, Distt. Sheikhupura, Punjab."
            },
            "objective": "To apply my expertise in Python, Django (Web Development), and data science workflows alongside advanced skills in AI and Generative Models (LLMs, LoRA/QLoRA, RAG/CAG, NLP, AI agents, and prompt engineering) to build intelligent, data-driven solutions. I aim to leverage my experience in data analysis, visualization (Power BI, Tableau, Plotly), cloud (AWS), and automation tools (n8n, data scraping) to solve real-world problems, enhance decision-making, and drive innovation in a forward-looking organization.",
            "profile": {
                "father_name": "Hadayat Ali",
                "date_of_birth": "Feb, 15, 1986.",
                "cnic": "35401-1249389-9",
                "marital_status": "Married",
                "domicile": "Sheikhupura (Punjab)",
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

        # Create Sample Projects
        projects_data = [
            {
                'title': 'AI-Powered Data Analysis Dashboard',
                'description': 'A comprehensive dashboard built with Django and integrated with machine learning models for predictive analytics. Features real-time data visualization using Plotly and advanced AI algorithms for pattern recognition.',
                'technologies': 'Django, Python, Machine Learning, Plotly, Pandas, NumPy',
                'featured': True
            },
            {
                'title': 'E-commerce Web Application',
                'description': 'Full-stack e-commerce platform with Django backend, featuring user authentication, payment integration, and inventory management system.',
                'technologies': 'Django, HTML, CSS, JavaScript, PostgreSQL',
                'featured': True
            },
            {
                'title': 'NLP Text Analysis Tool',
                'description': 'Natural Language Processing application for sentiment analysis and text classification using advanced AI models and prompt engineering techniques.',
                'technologies': 'Python, NLP, AI, Django, Machine Learning',
                'featured': False
            }
        ]

        for project in projects_data:
            Project.objects.create(**project)
            self.stdout.write(f'Created project: {project["title"]}')

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

