from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    """
    Site Settings Model - Singleton pattern for site configuration
    """
    
    # Basic Site Information
    site_name = models.CharField(
        max_length=100,
        default="Al Aqsa School",
        verbose_name=_("Site Name"),
        help_text=_("The name of your school/institution")
    )
    
    site_tagline = models.CharField(
        max_length=200,
        default="Islamic Educational Excellence",
        verbose_name=_("Site Tagline"),
        help_text=_("A short tagline describing your institution")
    )
    
    site_description = models.TextField(
        max_length=500,
        default="Nurturing Islamic character while achieving academic excellence. We provide a comprehensive Islamic education that prepares students for both this world and the hereafter.",
        verbose_name=_("Site Description"),
        help_text=_("A brief description of your institution")
    )
    
    # Logo and Branding
    logo = models.ImageField(
        upload_to='site/logo/',
        null=True,
        blank=True,
        verbose_name=_("Site Logo"),
        help_text=_("Upload your institution logo (recommended size: 200x80px)")
    )
    
    favicon = models.ImageField(
        upload_to='site/favicon/',
        null=True,
        blank=True,
        verbose_name=_("Favicon"),
        help_text=_("Upload favicon (recommended size: 32x32px)")
    )
    
    # Contact Information
    address = models.TextField(
        max_length=500,
        default="123 Islamic Street, Dhaka, Bangladesh",
        verbose_name=_("Address"),
        help_text=_("Complete address of your institution")
    )
    
    phone = models.CharField(
        max_length=20,
        default="+880 1234-567890",
        verbose_name=_("Phone Number"),
        help_text=_("Primary contact phone number")
    )
    
    email = models.EmailField(
        default="info@alaqsaschool.edu.bd",
        verbose_name=_("Email Address"),
        help_text=_("Primary contact email address")
    )
    
    # Additional Contact Details
    emergency_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Emergency Phone"),
        help_text=_("Emergency contact number")
    )
    
    fax = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Fax Number"),
        help_text=_("Fax number if available")
    )
    
    # Business Hours
    office_hours = models.TextField(
        max_length=200,
        default="Sunday - Thursday: 8:00 AM - 4:00 PM",
        verbose_name=_("Office Hours"),
        help_text=_("Business/office hours")
    )
    
    # Social Media Links
    facebook_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Facebook URL"),
        help_text=_("Your Facebook page URL")
    )
    
    twitter_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Twitter URL"),
        help_text=_("Your Twitter profile URL")
    )
    
    instagram_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Instagram URL"),
        help_text=_("Your Instagram profile URL")
    )
    
    youtube_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("YouTube URL"),
        help_text=_("Your YouTube channel URL")
    )
    
    linkedin_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("LinkedIn URL"),
        help_text=_("Your LinkedIn profile URL")
    )
    
    # SEO Settings
    meta_title = models.CharField(
        max_length=60,
        default="Al Aqsa School - Islamic Educational Institution",
        verbose_name=_("Meta Title"),
        help_text=_("SEO title (max 60 characters)")
    )
    
    meta_description = models.TextField(
        max_length=160,
        default="Al Aqsa School provides comprehensive Islamic education with academic excellence. Join us for quality education in a nurturing Islamic environment.",
        verbose_name=_("Meta Description"),
        help_text=_("SEO description (max 160 characters)")
    )
    
    meta_keywords = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Meta Keywords"),
        help_text=_("SEO keywords (comma-separated)")
    )
    
    google_analytics_code = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Google Analytics Code"),
        help_text=_("Google Analytics tracking code")
    )
    
    google_verification_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Google Verification Code"),
        help_text=_("Google Search Console verification code")
    )
    
    # Additional Settings
    copyright_text = models.CharField(
        max_length=200,
        default="© 2025 Al Aqsa School. All rights reserved.",
        verbose_name=_("Copyright Text"),
        help_text=_("Copyright notice text")
    )
    
    privacy_policy_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Privacy Policy URL"),
        help_text=_("URL to privacy policy page")
    )
    
    terms_of_service_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Terms of Service URL"),
        help_text=_("URL to terms of service page")
    )
    
    # Prayer Times Settings
    show_prayer_times = models.BooleanField(
        default=True,
        verbose_name=_("Show Prayer Times"),
        help_text=_("Display prayer times widget on website")
    )
    
    prayer_times_api_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Prayer Times API URL"),
        help_text=_("API URL for fetching prayer times")
    )
    
    # System Settings
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Site Active"),
        help_text=_("Enable/disable the website")
    )
    
    maintenance_mode = models.BooleanField(
        default=False,
        verbose_name=_("Maintenance Mode"),
        help_text=_("Put website in maintenance mode")
    )
    
    maintenance_message = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Maintenance Message"),
        help_text=_("Message to display during maintenance")
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.site_name} - Site Settings"
    
    def save(self, *args, **kwargs):
        """Ensure only one instance exists (Singleton pattern)"""
        if not self.pk and SiteSettings.objects.exists():
            # If this is a new instance and another exists, don't save
            return
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get the site settings instance, create if doesn't exist"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Al Aqsa School',
                'site_tagline': 'Islamic Educational Excellence',
                'site_description': 'Nurturing Islamic character while achieving academic excellence.',
                'address': '123 Islamic Street, Dhaka, Bangladesh',
                'phone': '+880 1234-567890',
                'email': 'info@alaqsaschool.edu.bd',
                'office_hours': 'Sunday - Thursday: 8:00 AM - 4:00 PM',
                'meta_title': 'Al Aqsa School - Islamic Educational Institution',
                'meta_description': 'Al Aqsa School provides comprehensive Islamic education with academic excellence.',
                'copyright_text': '© 2025 Al Aqsa School. All rights reserved.',
            }
        )
        return settings
    
    def get_social_media_links(self):
        """Get all non-empty social media links"""
        social_links = {}
        if self.facebook_url:
            social_links['facebook'] = self.facebook_url
        if self.twitter_url:
            social_links['twitter'] = self.twitter_url
        if self.instagram_url:
            social_links['instagram'] = self.instagram_url
        if self.youtube_url:
            social_links['youtube'] = self.youtube_url
        if self.linkedin_url:
            social_links['linkedin'] = self.linkedin_url
        return social_links


class ContactMessage(models.Model):
    """
    Model to store contact form messages
    """
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    
    STATUS_CHOICES = [
        ('new', _('New')),
        ('read', _('Read')),
        ('replied', _('Replied')),
        ('closed', _('Closed')),
    ]
    
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone"))
    subject = models.CharField(max_length=200, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name=_("Priority")
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name=_("Status")
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("IP Address"))
    user_agent = models.TextField(blank=True, null=True, verbose_name=_("User Agent"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"


class NewsletterSubscription(models.Model):
    """
    Model to store newsletter subscriptions
    """
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Subscribed At"))
    unsubscribed_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Unsubscribed At"))
    
    class Meta:
        verbose_name = _("Newsletter Subscription")
        verbose_name_plural = _("Newsletter Subscriptions")
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
