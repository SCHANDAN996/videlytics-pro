from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import os
import json
from django.http import JsonResponse
# from .youtube_api import get_channel_details # Abhi ke liye comment rakhein
# from .models import Wallet # Abhi ke liye comment rakhein
from decimal import Decimal

# Home Page View - Login zaroori hai
@login_required
def home_view(request):
    # wallet = Wallet.objects.get(user=request.user)
    # context = {'wallet_balance': wallet.balance}
    context = {'wallet_balance': '10.00'} # Abhi ke liye dummy data
    return render(request, 'index.html', context)

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
    return render(request, 'registration/register.html', {'form': form})

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
    return render(request, 'registration/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# API View - Channel data ke liye
@login_required
def analyze_channel_view(request):
    # wallet = Wallet.objects.get(user=request.user)
    analysis_cost = Decimal('0.25')

    # if wallet.balance < analysis_cost:
    #     return JsonResponse({'error': 'Insufficient balance. Please add funds to your wallet.'}, status=402)

    if request.method == 'POST':
        data = json.loads(request.body)
        channel_url = data.get('channel_url')
        api_key = os.environ.get('YOUTUBE_API_KEY')

        if not channel_url or not api_key:
            return JsonResponse({'error': 'Channel URL or API Key is missing'}, status=400)
        
        # Abhi ke liye dummy data
        channel_data = {
            'title': 'Dummy Channel', 'thumbnail': 'https://via.placeholder.com/80',
            'subscribers': '1000000', 'views': '50000000', 'videos': '1500',
            'channelId': 'UC-dummy-id'
        }
        # channel_data = get_channel_details(api_key, channel_url)

        # if channel_data.get('error'):
        #     return JsonResponse(channel_data, status=400)

        # wallet.balance -= analysis_cost
        # wallet.save()

        # channel_data['new_balance'] = wallet.balance
        return JsonResponse(channel_data)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
