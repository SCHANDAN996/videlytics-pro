from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True 
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-for-debugging')
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'videlytics_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Base templates ke liye
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- YEH DO LINEIN BAHUT ZAROORI HAIN ---
LOGIN_URL = 'login' 
LOGIN_REDIRECT_URL = 'home'

    # ... (upar ka code waisa hi rahega) ...
     
     INSTALLED_APPS = [
         'django.contrib.admin',
         'django.contrib.auth',
         'django.contrib.contenttypes',
         'django.contrib.sessions',
         'django.contrib.messages',
         'whitenoise.runserver_nostatic',
         'django.contrib.staticfiles',
         'main_app',
         'crispy_forms',           # Naya app jodein
         'crispy_tailwind',      # Naya app jodein
     ]
     
     # file ke sabse neeche yeh do linein jodein
     CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
     CRISPY_TEMPLATE_PACK = "tailwind"
     
     # ... (baki ka code waisa hi rahega) ...
     

