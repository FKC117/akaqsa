from django.urls import path
from website import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('student-life/', views.student_life, name='student_life'),
    path('admissions/', views.admissions, name='admissions'),
    path('parent-portal/', views.parent_portal, name='parent_portal'),
    path('contact/', views.contact, name='contact'),
    path('api/prayer-times/', views.prayer_times, name='prayer_times'),
]