from django.urls import path
from . import views

urlpatterns = [
    # Home page (dashboard)
    path('', views.home_view, name='home'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # API URL for channel analysis
    path('api/analyze_channel/', views.analyze_channel_view, name='analyze_channel'),
]