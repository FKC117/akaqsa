from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
import json

from .models import SiteSettings, ContactMessage, NewsletterSubscription
from .forms import ContactForm, NewsletterSubscriptionForm, SearchForm, FeedbackForm


def get_site_settings():
    """Helper function to get site settings"""
    return SiteSettings.get_settings()


def index(request):
    """Homepage view - main landing page"""
    site_settings = get_site_settings()
    
    # Check if site is in maintenance mode
    if site_settings.maintenance_mode and not request.user.is_staff:
        return render(request, 'website/maintenance.html', {
            'site_settings': site_settings
        })
    
    context = {
        'site_settings': site_settings,
        'page_title': site_settings.meta_title,
        'page_description': site_settings.meta_description,
    }
    return render(request, 'website/index.html', context)


def about(request):
    """About Us page"""
    site_settings = get_site_settings()
    context = {
        'site_settings': site_settings,
        'page_title': f"About Us - {site_settings.site_name}",
        'page_description': f"Learn more about {site_settings.site_name} and our mission to provide Islamic education.",
    }
    return render(request, 'website/about.html', context)


def programs(request):
    """Academic Programs page"""
    site_settings = get_site_settings()
    context = {
        'site_settings': site_settings,
        'page_title': f"Academic Programs - {site_settings.site_name}",
        'page_description': f"Explore the academic programs and Islamic curriculum offered at {site_settings.site_name}.",
    }
    return render(request, 'website/programs.html', context)


def student_life(request):
    """Student Life page"""
    site_settings = get_site_settings()
    context = {
        'site_settings': site_settings,
        'page_title': f"Student Life - {site_settings.site_name}",
        'page_description': f"Discover student life and activities at {site_settings.site_name}.",
    }
    return render(request, 'website/student_life.html', context)


def admissions(request):
    """Admissions page"""
    site_settings = get_site_settings()
    context = {
        'site_settings': site_settings,
        'page_title': f"Admissions - {site_settings.site_name}",
        'page_description': f"Apply for admission to {site_settings.site_name}. Learn about our admission process and requirements.",
    }
    return render(request, 'website/admissions.html', context)


def parent_portal(request):
    """Parent Portal page"""
    site_settings = get_site_settings()
    context = {
        'site_settings': site_settings,
        'page_title': f"Parent Portal - {site_settings.site_name}",
        'page_description': f"Access the parent portal for {site_settings.site_name} to stay connected with your child's education.",
    }
    return render(request, 'website/parent_portal.html', context)


def contact(request):
    """Contact page with contact form"""
    site_settings = get_site_settings()
    
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_message = contact_form.save(commit=False)
            
            # Capture IP address and user agent
            contact_message.ip_address = get_client_ip(request)
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            contact_message.save()
            
            # Send email notification (if configured)
            if hasattr(settings, 'CONTACT_EMAIL') and settings.CONTACT_EMAIL:
                try:
                    send_mail(
                        subject=f"New Contact Message: {contact_message.subject}",
                        message=f"""
                        New contact message received:
                        
                        Name: {contact_message.name}
                        Email: {contact_message.email}
                        Phone: {contact_message.phone or 'Not provided'}
                        Subject: {contact_message.subject}
                        Message: {contact_message.message}
                        
                        IP Address: {contact_message.ip_address}
                        Date: {contact_message.created_at}
                        """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.CONTACT_EMAIL],
                        fail_silently=True,
                    )
                except Exception as e:
                    # Log the error but don't break the form submission
                    print(f"Error sending contact email: {e}")
            
            messages.success(request, _('Thank you for your message! We will get back to you soon.'))
            return redirect('website:contact')
    else:
        contact_form = ContactForm()
    
    context = {
        'site_settings': site_settings,
        'contact_form': contact_form,
        'page_title': f"Contact Us - {site_settings.site_name}",
        'page_description': f"Get in touch with {site_settings.site_name}. Contact us for inquiries, admissions, or general information.",
    }
    return render(request, 'website/contact.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Newsletter subscription endpoint"""
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save()
            return JsonResponse({
                'success': True,
                'message': _('Thank you for subscribing to our newsletter!')
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def prayer_times(request):
    """API endpoint for prayer times"""
    site_settings = get_site_settings()
    
    if not site_settings.show_prayer_times:
        return JsonResponse({'error': 'Prayer times are disabled'}, status=404)
    
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


def search(request):
    """Search functionality"""
    site_settings = get_site_settings()
    search_form = SearchForm(request.GET)
    results = []
    
    if search_form.is_valid():
        query = search_form.cleaned_data['q']
        # Implement search logic here
        # For now, just return empty results
        results = []
    
    context = {
        'site_settings': site_settings,
        'search_form': search_form,
        'results': results,
        'query': request.GET.get('q', ''),
        'page_title': f"Search Results - {site_settings.site_name}",
    }
    return render(request, 'website/search.html', context)


def feedback(request):
    """Feedback form page"""
    site_settings = get_site_settings()
    
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            # Process feedback (save to database, send email, etc.)
            messages.success(request, _('Thank you for your feedback!'))
            return redirect('website:feedback')
    else:
        feedback_form = FeedbackForm()
    
    context = {
        'site_settings': site_settings,
        'feedback_form': feedback_form,
        'page_title': f"Feedback - {site_settings.site_name}",
    }
    return render(request, 'website/feedback.html', context)


def maintenance(request):
    """Maintenance page"""
    site_settings = get_site_settings()
    context = {
        'site_settings': site_settings,
        'page_title': f"Under Maintenance - {site_settings.site_name}",
    }
    return render(request, 'website/maintenance.html', context)


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Context processor to make site settings available globally
def site_settings_context(request):
    """Context processor to add site settings to all templates"""
    try:
        site_settings = SiteSettings.get_settings()
        return {
            'site_settings': site_settings,
            'social_links': site_settings.get_social_media_links(),
        }
    except Exception:
        # Return empty dict if site settings don't exist yet
        return {
            'site_settings': None,
            'social_links': {},
        }
