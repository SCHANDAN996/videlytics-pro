from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # main_app ke URLs ko include karein
    path('', include('main_app.urls')),
    # Django ke default auth URLs (login, logout, etc.) ko include karein
    path('accounts/', include('django.contrib.auth.urls')),
]
