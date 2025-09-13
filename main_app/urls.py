from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home_view, name='home'),
    path('pricing/', views.pricing_view, name='pricing'),

    # Auth URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Static Pages URLs
    path('about/', views.about_view, name='about'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),

    # API URL
    path('api/analyze_channel/', views.analyze_channel_view, name='analyze_channel'),
]