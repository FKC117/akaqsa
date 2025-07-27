from django import forms
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage, NewsletterSubscription


class ContactForm(forms.ModelForm):
    """
    Contact form for website visitors
    """
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your full name'),
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('your.email@example.com'),
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your phone number (optional)')
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Subject of your message'),
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Your message here...'),
                'required': True
            }),
        }
        labels = {
            'name': _('Full Name'),
            'email': _('Email Address'),
            'phone': _('Phone Number'),
            'subject': _('Subject'),
            'message': _('Message'),
        }
    
    def clean_name(self):
        """Validate name field"""
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError(_('Name must be at least 2 characters long.'))
        return name.strip()
    
    def clean_subject(self):
        """Validate subject field"""
        subject = self.cleaned_data.get('subject')
        if len(subject.strip()) < 5:
            raise forms.ValidationError(_('Subject must be at least 5 characters long.'))
        return subject.strip()
    
    def clean_message(self):
        """Validate message field"""
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise forms.ValidationError(_('Message must be at least 10 characters long.'))
        return message.strip()
    
    def clean_phone(self):
        """Validate phone number (optional)"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove spaces, dashes, and parentheses
            import re
            phone = re.sub(r'[\s\-\(\)]', '', phone)
            if not re.match(r'^\+?[\d\s\-\(\)]{10,15}$', phone):
                raise forms.ValidationError(_('Please enter a valid phone number.'))
        return phone


class NewsletterSubscriptionForm(forms.ModelForm):
    """
    Newsletter subscription form
    """
    
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter your email address'),
                'required': True
            }),
        }
        labels = {
            'email': _('Email Address'),
        }
    
    def clean_email(self):
        """Validate email and check for existing subscription"""
        email = self.cleaned_data.get('email')
        
        # Check if already subscribed
        if NewsletterSubscription.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError(_('This email is already subscribed to our newsletter.'))
        
        return email.lower()
    
    def save(self, commit=True):
        """Save the subscription, deactivating any existing one first"""
        email = self.cleaned_data['email']
        
        # Deactivate any existing subscription
        NewsletterSubscription.objects.filter(email=email).update(is_active=False)
        
        # Create new subscription
        return super().save(commit=commit)


class SiteSettingsForm(forms.ModelForm):
    """
    Form for updating site settings (admin use)
    """
    
    class Meta:
        model = ContactMessage  # This will be updated to SiteSettings when needed
        fields = '__all__'
        exclude = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.URLInput)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control', 'rows': 3})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})


class SearchForm(forms.Form):
    """
    Search form for website
    """
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search...'),
            'aria-label': _('Search')
        }),
        label=_('Search')
    )
    
    def clean_q(self):
        """Clean search query"""
        query = self.cleaned_data.get('q', '').strip()
        if len(query) < 2:
            raise forms.ValidationError(_('Search query must be at least 2 characters long.'))
        return query


class FeedbackForm(forms.Form):
    """
    Feedback form for website visitors
    """
    FEEDBACK_TYPE_CHOICES = [
        ('general', _('General Feedback')),
        ('bug', _('Bug Report')),
        ('feature', _('Feature Request')),
        ('complaint', _('Complaint')),
        ('compliment', _('Compliment')),
    ]
    
    RATING_CHOICES = [
        (5, _('Excellent')),
        (4, _('Very Good')),
        (3, _('Good')),
        (2, _('Fair')),
        (1, _('Poor')),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your name')
        }),
        label=_('Name')
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('your.email@example.com')
        }),
        label=_('Email')
    )
    
    feedback_type = forms.ChoiceField(
        choices=FEEDBACK_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Feedback Type')
    )
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Rating'),
        required=False
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': _('Please share your feedback...')
        }),
        label=_('Message')
    )
    
    def clean_message(self):
        """Validate message length"""
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise forms.ValidationError(_('Message must be at least 10 characters long.'))
        return message.strip() 