from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Plan, Subscription, UserProfile
from .youtube_api import YouTubeChannelAnalyzer # Assuming youtube_api.py is updated
import razorpay
import json
import os

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(os.environ.get('RAZORPAY_KEY_ID'), os.environ.get('RAZORPAY_KEY_SECRET'))
)

def landing_page_view(request):
    """ Public landing page """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

@login_required
def dashboard_view(request):
    """ Main dashboard for logged-in users """
    try:
        active_subscription = Subscription.objects.get(user=request.user, is_active=True)
    except Subscription.DoesNotExist:
        active_subscription = None
    
    context = {
        'subscription': active_subscription,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def pricing_view(request):
    """ Display subscription plans """
    plans = Plan.objects.all().order_by('price')
    context = {'plans': plans}
    return render(request, 'dashboard/pricing.html', context)

@login_required
def create_subscription_view(request, plan_id):
    """ Create a Razorpay subscription order """
    if request.method == 'POST':
        plan = Plan.objects.get(id=plan_id)
        
        # Data for creating subscription in Razorpay
        subscription_data = {
            'plan_id': plan.razorpay_plan_id,
            'total_count': 12, # For a 1-year plan with monthly payments
            'quantity': 1,
        }
        
        try:
            subscription = razorpay_client.subscription.create(subscription_data)
            
            context = {
                'subscription_id': subscription['id'],
                'razorpay_key_id': os.environ.get('RAZORPAY_KEY_ID'),
                'plan_name': plan.name,
                'user_name': request.user.username,
                'user_email': request.user.email,
            }
            return render(request, 'dashboard/payment.html', context)
            
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return redirect('pricing')

@login_required
def subscription_success_view(request):
    """ Handle successful payment and activate subscription """
    if request.method == 'POST':
        data = request.POST
        razorpay_subscription_id = data.get('razorpay_subscription_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        params_dict = {
            'razorpay_subscription_id': razorpay_subscription_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            # Verify the payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Find the plan associated with the razorpay subscription
            sub_details = razorpay_client.subscription.fetch(razorpay_subscription_id)
            razorpay_plan_id = sub_details['plan_id']
            plan = Plan.objects.get(razorpay_plan_id=razorpay_plan_id)

            # Deactivate any old subscriptions
            Subscription.objects.filter(user=request.user, is_active=True).update(is_active=False)

            # Create new subscription
            Subscription.objects.create(
                user=request.user,
                plan=plan,
                razorpay_subscription_id=razorpay_subscription_id,
                end_date=timezone.now() + timedelta(days=30), # Or based on plan
                is_active=True,
            )
            return redirect('dashboard')

        except Exception as e:
            # Handle payment failure
            return render(request, 'dashboard/payment_failed.html', {'error': str(e)})

    return redirect('pricing')


@login_required
def analyze_channel_view(request):
    """
    View for the YouTube Analyzer tool.
    Checks for active subscription.
    """
    try:
        subscription = Subscription.objects.get(user=request.user, is_active=True)
    except Subscription.DoesNotExist:
        return redirect('pricing') # Redirect to pricing if no active subscription

    # Your existing analysis logic goes here
    # ...
    # Return the analysis_results.html template
    context = {'subscription': subscription}
    return render(request, 'dashboard/analyzer_tool.html', context)

@login_required
def profile_view(request):
    """ User profile and referral page """
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'dashboard/profile.html', context)
