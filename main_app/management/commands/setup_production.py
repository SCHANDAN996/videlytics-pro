import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Runs all necessary commands to set up the application for production.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting production setup...'))

        # 1. Apply database migrations
        self.stdout.write('Applying database migrations...')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Database migrations applied successfully.'))

        # 2. Create a superuser from environment variables
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
            self.stdout.write(self.style.ERROR('Superuser environment variables not set. Skipping superuser creation.'))

        self.stdout.write(self.style.SUCCESS('Production setup finished!'))
