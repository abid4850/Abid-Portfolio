from django.conf import settings
from .models import Profile

def site_profile(request):
    """Provide site-wide metadata and profile to all templates."""
    try:
        profile = Profile.objects.first()
    except:
        profile = None
    
    site_url = f"{request.scheme}://{request.get_host()}"
    
    return {
        'site_profile': profile,
        'site_url': site_url,
        'meta_title': getattr(profile, 'name', 'Abid Hussain') + ' - Portfolio',
        'meta_description': getattr(profile, 'objective', 'Python Developer, Data Scientist, and AI Specialist'),
        'meta_image': f"{site_url}{profile.profile_image.url}" if profile and profile.profile_image else f"{site_url}/static/professional_headshot.jpg",
        'meta_keywords': 'Python, Django, Data Science, AI, Machine Learning, Web Development',
        'meta_author': getattr(profile, 'name', 'Abid Hussain'),
    }
