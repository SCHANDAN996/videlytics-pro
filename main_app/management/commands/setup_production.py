import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings

class Command(BaseCommand):
    help = 'Runs all necessary commands to set up the application for production.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Starting production setup ---'))

        # 1. Apply database migrations
        self.stdout.write('Step 1: Applying database migrations...')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Database migrations applied successfully.'))

        # 2. Ensure the Site object is correctly configured
        self.stdout.write('Step 2: Configuring site domain...')
        try:
            site = Site.objects.get(pk=settings.SITE_ID)
            site.domain = 'videlytics.pro'
            site.name = 'Videlytics.pro'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Site domain updated to {site.domain}'))
        except Site.DoesNotExist:
            self.stdout.write(self.style.WARNING('Site not found, creating a new one.'))
            Site.objects.create(pk=settings.SITE_ID, domain='videlytics.pro', name='Videlytics.pro')
            self.stdout.write(self.style.SUCCESS('Site created successfully.'))

        # 3. Create a superuser from environment variables
        self.stdout.write('Step 3: Creating superuser...')
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if username and email and password:
            if not User.objects.filter(username=username).exists():
                self.stdout.write(f'Creating superuser "{username}"...')
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
        else:
            self.stdout.write(self.style.ERROR('Superuser environment variables not set. Skipping.'))

        self.stdout.write(self.style.SUCCESS('--- Production setup finished successfully! ---'))

