from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import os
import json
from .youtube_api import get_channel_details # Ise import karein

# Home Page View - Login zaroori hai
@login_required
def home_view(request):
    return render(request, 'index.html')

# Register View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout View (NAYA FUNCTION)
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    # Agar GET request hai to bhi logout kar dein (optional, for convenience)
    logout(request)
    return redirect('login')


# API View - Channel data ke liye
@login_required
def analyze_channel_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        channel_url = data.get('channel_url')
        api_key = os.environ.get('YOUTUBE_API_KEY')

        if not channel_url or not api_key:
            return JsonResponse({'error': 'Channel URL or API Key is missing'}, status=400)

        channel_data = get_channel_details(api_key, channel_url)

        if channel_data.get('error'):
            return JsonResponse(channel_data, status=400)

        return JsonResponse(channel_data)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
