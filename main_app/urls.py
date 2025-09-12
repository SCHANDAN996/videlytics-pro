from django.urls import path
from .views import home_view, register_view, login_view, logout_view, analyze_channel_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    # Naya logout URL
    path('logout/', logout_view, name='logout'),
    path('api/analyze_channel/', analyze_channel_view, name='analyze_channel'),
]
