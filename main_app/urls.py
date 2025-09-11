from django.urls import path
from .views import home_view, register_view, login_view, logout_view

urlpatterns = [
    # Purana home page ka URL
    path('', home_view, name='home'),
    
    # Naye URLs registration, login, aur logout ke liye
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]


