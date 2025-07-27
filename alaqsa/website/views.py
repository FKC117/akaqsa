from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import json

def index(request):
    """Homepage view - main landing page"""
    return render(request, 'website/index.html')

def about(request):
    """About Us page"""
    return render(request, 'website/about.html')

def programs(request):
    """Academic Programs page"""
    return render(request, 'website/programs.html')

def student_life(request):
    """Student Life page"""
    return render(request, 'website/student_life.html')

def admissions(request):
    """Admissions page"""
    return render(request, 'website/admissions.html')

def parent_portal(request):
    """Parent Portal page"""
    return render(request, 'website/parent_portal.html')

def contact(request):
    """Contact page"""
    return render(request, 'website/contact.html')

def prayer_times(request):
    """API endpoint for prayer times"""
    # This would typically fetch from a prayer times API
    # For now, returning sample data
    prayer_times = {
        'fajr': '5:30 AM',
        'dhuhr': '12:30 PM',
        'asr': '3:45 PM',
        'maghrib': '6:15 PM',
        'isha': '7:45 PM',
        'next_prayer': 'Asr',
        'next_time': '3:45 PM'
    }
    return JsonResponse(prayer_times)
