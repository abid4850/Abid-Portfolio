from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['portfolio:home', 'portfolio:about', 'portfolio:projects', 'portfolio:services', 'portfolio:skills', 'portfolio:contact']

    def location(self, item):
        return reverse(item.replace('portfolio:', ''))

class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return reverse('portfolio:project_detail', args=[str(obj.id)])