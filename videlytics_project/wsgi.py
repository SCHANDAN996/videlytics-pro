# Web Server Gateway Interface (WSGI) config for videlytics_project project.
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videlytics_project.settings')

application = get_wsgi_application()
