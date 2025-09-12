"""
Django settings for videlytics_project project.
... (upar ka code waisa hi rahega) ...
"""

from pathlib import Path
import os

# ... (sara purana code waisa hi rahega) ...

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- YEH DO NAYI LINEIN JODEIN ---
LOGIN_URL = 'login' # Batayein ki login page ka naam 'login' hai
LOGIN_REDIRECT_URL = 'home' # Batayein ki login ke baad 'home' page par jana hai

