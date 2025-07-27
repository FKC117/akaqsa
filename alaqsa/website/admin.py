from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings, ContactMessage, NewsletterSubscription


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin configuration for SiteSettings model"""
    
    def has_add_permission(self, request):
        """Only allow one instance of SiteSettings"""
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of SiteSettings"""
        return False
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'site_name', 'site_tagline', 'site_description',
                'is_active', 'maintenance_mode', 'maintenance_message'
            )
        }),
        (_('Logo & Branding'), {
            'fields': ('logo', 'favicon'),
            'classes': ('collapse',)
        }),
        (_('Contact Information'), {
            'fields': (
                'address', 'phone', 'email', 'emergency_phone', 'fax', 'office_hours'
            )
        }),
        (_('Social Media'), {
            'fields': (
                'facebook_url', 'twitter_url', 'instagram_url', 
                'youtube_url', 'linkedin_url'
            ),
            'classes': ('collapse',)
        }),
        (_('SEO Settings'), {
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'google_analytics_code', 'google_verification_code'
            ),
            'classes': ('collapse',)
        }),
        (_('Prayer Times'), {
            'fields': ('show_prayer_times', 'prayer_times_api_url'),
            'classes': ('collapse',)
        }),
        (_('Legal & Footer'), {
            'fields': (
                'copyright_text', 'privacy_policy_url', 'terms_of_service_url'
            ),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'readonly_fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    list_display = ('site_name', 'site_tagline', 'is_active', 'maintenance_mode', 'updated_at')
    list_filter = ('is_active', 'maintenance_mode', 'show_prayer_times')
    search_fields = ('site_name', 'site_tagline', 'email', 'phone')
    
    def changelist_view(self, request, extra_context=None):
        """Custom changelist view to handle singleton pattern"""
        # If no SiteSettings exist, redirect to add view
        if not SiteSettings.objects.exists():
            return self.add_view(request)
        
        # If only one exists, redirect to change view
        site_settings = SiteSettings.objects.first()
        return self.response_change(request, site_settings)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin configuration for ContactMessage model"""
    
    list_display = (
        'name', 'email', 'subject', 'priority', 'status', 
        'created_at', 'get_short_message'
    )
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('ip_address', 'user_agent', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Message Details'), {
            'fields': ('name', 'email', 'phone', 'subject', 'message')
        }),
        (_('Status & Priority'), {
            'fields': ('priority', 'status')
        }),
        (_('Technical Information'), {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_closed']
    
    def get_short_message(self, obj):
        """Display truncated message"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    get_short_message.short_description = _('Message Preview')
    
    def mark_as_read(self, request, queryset):
        """Mark selected messages as read"""
        updated = queryset.update(status='read')
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = _('Mark selected messages as read')
    
    def mark_as_replied(self, request, queryset):
        """Mark selected messages as replied"""
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} message(s) marked as replied.')
    mark_as_replied.short_description = _('Mark selected messages as replied')
    
    def mark_as_closed(self, request, queryset):
        """Mark selected messages as closed"""
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} message(s) marked as closed.')
    mark_as_closed.short_description = _('Mark selected messages as closed')


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    """Admin configuration for NewsletterSubscription model"""
    
    list_display = ('email', 'is_active', 'subscribed_at', 'unsubscribed_at')
    list_filter = ('is_active', 'subscribed_at', 'unsubscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    date_hierarchy = 'subscribed_at'
    
    fieldsets = (
        (_('Subscription Details'), {
            'fields': ('email', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        """Activate selected subscriptions"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscription(s) activated.')
    activate_subscriptions.short_description = _('Activate selected subscriptions')
    
    def deactivate_subscriptions(self, request, queryset):
        """Deactivate selected subscriptions"""
        from django.utils import timezone
        updated = queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, f'{updated} subscription(s) deactivated.')
    deactivate_subscriptions.short_description = _('Deactivate selected subscriptions')


# Customize admin site
admin.site.site_header = _('Al Aqsa School Administration')
admin.site.site_title = _('Al Aqsa School Admin')
admin.site.index_title = _('Welcome to Al Aqsa School Administration')
