from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('api/create_order/', views.create_order_view, name='create_order'),
    path('payment/handler/', views.payment_handler_view, name='payment_handler'),
    path('api/analyze_channel/', views.analyze_channel_view, name='analyze_channel'),
]
