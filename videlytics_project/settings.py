from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG को False ही रहने दें, लेकिन एरर देखने के लिए अस्थायी रूप से True कर सकते हैं
DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']

# --- यहाँ बदलाव करें ---
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# अपने कस्टम डोमेन को यहाँ जोड़ें
ALLOWED_HOSTS.extend(['videlytics.pro', 'www.videlytics.pro'])
# --- बदलाव समाप्त ---


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Whitenoise static files
    'django.contrib.staticfiles',
    
    # My Apps
    'main_app',
    
    # 3rd Party Apps
    'crispy_forms',
    'crispy_tailwind',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# ... (बाकी फ़ाइल वैसी ही रहेगी) ...
