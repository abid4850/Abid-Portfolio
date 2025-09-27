from django.urls import path
from . import views

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
]

