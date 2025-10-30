from django.urls import path
from . import views
from .views.robots import robots_txt

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact, name='contact'),
    path('api/skills/', views.api_skills, name='api_skills'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

