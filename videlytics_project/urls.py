from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')), # Sabhi requests ko main_app ko bhej do
    path('accounts/', include('django.contrib.auth.urls')), # Django ke bane-banaye auth URLs
]


