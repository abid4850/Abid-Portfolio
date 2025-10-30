from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from ..models import Profile, SkillCategory, Skill, Education, Project, Service, Contact
from ..models import Blog

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

def contact(request):
    """Contact page"""
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            
            Contact.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, 'Message sent successfully!')
            return render(request, 'portfolio/contact.html')
            
        return render(request, 'portfolio/contact.html')
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def blogs(request):
    """List of blog posts"""
    try:
        posts = Blog.objects.all()
        return render(request, 'portfolio/blogs.html', {'posts': posts, 'profile': Profile.objects.first()})
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def blog_detail(request, slug):
    """Individual blog post"""
    try:
        post = get_object_or_404(Blog, slug=slug)
        return render(request, 'portfolio/blog_detail.html', {'post': post, 'profile': Profile.objects.first()})
    except Exception as e:
        return render(request, 'portfolio/error.html', {'error': str(e)})

def api_skills(request):
    """API endpoint for skills"""
    try:
        categories = SkillCategory.objects.prefetch_related('skills').all()
        data = []
        for category in categories:
            skills = [{'name': skill.name, 'proficiency': skill.proficiency} 
                     for skill in category.skills.all()]
            data.append({
                'name': category.name,
                'skills': skills
            })
        return JsonResponse({'categories': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)