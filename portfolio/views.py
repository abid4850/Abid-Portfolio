from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Profile, SkillCategory, Skill, Education, Project, Service, Contact
from .models import Blog

def home(request):
    """Home page view with all portfolio sections"""
    try:
        profile = Profile.objects.first()
        skill_categories = SkillCategory.objects.prefetch_related('skills').all()
        education = Education.objects.all().order_by('-year')
        featured_projects = Project.objects.filter(featured=True)[:3]
        services = Service.objects.all()
        
        context = {
            'profile': profile,
            'skill_categories': skill_categories,
            'education': education,
            'featured_projects': featured_projects,
            'services': services,
        }
        
        return render(request, 'portfolio/home.html', context)
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def about(request):
    """About page with detailed profile information"""
    try:
        profile = Profile.objects.first()
        context = {
            'profile': profile,
        }
        return render(request, 'portfolio/about.html', context)
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def skills(request):
    """Skills page with detailed skill breakdown"""
    try:
        skill_categories = SkillCategory.objects.prefetch_related('skills').all()
        context = {
            'skill_categories': skill_categories,
        }
        return render(request, 'portfolio/skills.html', context)
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def projects(request):
    """Projects page with all projects"""
    try:
        all_projects = Project.objects.all()
        context = {
            'projects': all_projects,
        }
        return render(request, 'portfolio/projects.html', context)
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def project_detail(request, project_id):
    """Individual project detail page"""
    try:
        project = get_object_or_404(Project, id=project_id)
        context = {
            'project': project,
        }
        return render(request, 'portfolio/project_detail.html', context)
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def services_view(request):
    """Services page"""
    try:
        services = Service.objects.all()
        context = {
            'services': services,
        }
        return render(request, 'portfolio/services.html', context)
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def blogs(request):
    """List of blog posts - only published posts"""
    try:
        # Filter only published posts (published_date is in the past)
        from django.utils import timezone
        posts = Blog.objects.select_related('author').filter(
            published_date__lte=timezone.now().date()
        ).order_by('-published_date', '-created_at')
        
        # Handle draft posts (published_date is null)
        draft_posts = Blog.objects.select_related('author').filter(
            published_date__isnull=True
        ).order_by('-created_at')
        
        # Combine both querysets with published first
        posts = posts | draft_posts
        
        return render(request, 'portfolio/blogs.html', {
            'posts': posts, 
            'profile': Profile.objects.first()
        })
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})


def blog_detail(request, slug):
    """Display a single blog post"""
    try:
        post = get_object_or_404(Blog, slug=slug)
        return render(request, 'portfolio/blog_detail.html', {
            'post': post, 
            'profile': Profile.objects.first()
        })
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def contact(request):
    """Contact page with contact form"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            if name and email and subject and message:
                Contact.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                messages.success(request, 'Thank you for your message! I will get back to you soon.')
            else:
                messages.error(request, 'Please fill in all required fields.')
        except Exception as e:
            messages.error(request, 'An error occurred. Please try again.')
    
    try:
        profile = Profile.objects.first()
        context = {
            'profile': profile,
        }
        return render(request, 'portfolio/contact.html', context)
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

@csrf_exempt
def api_skills(request):
    """API endpoint for skills data"""
    try:
        skill_categories = SkillCategory.objects.prefetch_related('skills').all()
        data = []
        
        for category in skill_categories:
            category_data = {
                'name': category.name,
                'icon': category.icon,
                'skills': []
            }
            
            for skill in category.skills.all():
                category_data['skills'].append({
                    'name': skill.name,
                    'proficiency': skill.proficiency
                })
            
            data.append(category_data)
        
        return JsonResponse({'skill_categories': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
