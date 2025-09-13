from django.urls import path
from . import views

urlpatterns = [
    # Public Pages
    path('', views.landing_page_view, name='landing_page'),

    # Dashboard & Core App
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('profile/', views.profile_view, name='profile'),
    
    # Subscription & Payment
    path('subscription/create/<int:plan_id>/', views.create_subscription_view, name='create_subscription'),
    path('subscription/success/', views.subscription_success_view, name='subscription_success'),

    # Tools
    path('tools/youtube-analyzer/', views.analyze_channel_view, name='analyze_channel'),
    # Add other tools here in the future
]
