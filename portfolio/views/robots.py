from django.http import HttpResponse
from django.conf import settings

def robots_txt(request):
    site_url = f"{request.scheme}://{request.get_host()}"
    content = f"""User-agent: *
Allow: /
Disallow: /admin/

Sitemap: {site_url}/sitemap.xml"""
    return HttpResponse(content, content_type="text/plain")