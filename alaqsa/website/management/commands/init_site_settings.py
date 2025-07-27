from django.core.management.base import BaseCommand
from website.models import SiteSettings


class Command(BaseCommand):
    help = 'Initialize site settings with default values'

    def handle(self, *args, **options):
        try:
            # Check if site settings already exist
            if SiteSettings.objects.exists():
                self.stdout.write(
                    self.style.WARNING('Site settings already exist. Use admin panel to modify.')
                )
                return

            # Create default site settings
            site_settings = SiteSettings.objects.create(
                site_name='Al Aqsa School',
                site_tagline='Islamic Educational Excellence',
                site_description='Nurturing Islamic character while achieving academic excellence. We provide a comprehensive Islamic education that prepares students for both this world and the hereafter.',
                address='123 Islamic Street, Dhaka, Bangladesh',
                phone='+880 1234-567890',
                email='info@alaqsaschool.edu.bd',
                office_hours='Sunday - Thursday: 8:00 AM - 4:00 PM',
                meta_title='Al Aqsa School - Islamic Educational Institution',
                meta_description='Al Aqsa School provides comprehensive Islamic education with academic excellence. Join us for quality education in a nurturing Islamic environment.',
                meta_keywords='Islamic school, Islamic education, Al Aqsa, Bangladesh, Islamic curriculum',
                copyright_text='© 2025 Al Aqsa School. All rights reserved.',
                is_active=True,
                show_prayer_times=True,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created site settings for "{site_settings.site_name}"'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    'You can now customize these settings through the Django admin panel.'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating site settings: {str(e)}')
            ) 