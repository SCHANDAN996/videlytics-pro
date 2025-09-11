from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Hamara naya API logic import karein
from . import youtube_api

# Purane views waise hi rahenge...
def home_view(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('home')
    form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f"Welcome back, {user.username}!")
            return redirect('home')
    form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('home')


# YAHAN SE NAYA CODE SHURU HOTA HAI
# Yeh hamara naya API view hai
@csrf_exempt # Abhi ke liye security check ko bypass karein
def analyze_channel_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        channel_url = data.get('channel_url')

        if not channel_url:
            return JsonResponse({'error': 'Channel URL is required.'}, status=400)
        
        # URL se Channel ID nikalne ki koshish karein
        channel_id = youtube_api.get_channel_id_from_url(channel_url)

        if not channel_id:
            return JsonResponse({'error': 'Could not find a valid YouTube channel from this URL.'}, status=400)
        
        # Channel ID se details nikalne ki koshish karein
        channel_details = youtube_api.get_channel_details(channel_id)
        
        if 'error' in channel_details:
             return JsonResponse(channel_details, status=400)

        return JsonResponse(channel_details)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


