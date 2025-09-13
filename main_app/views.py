from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
import json
import razorpay
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .youtube_api import get_channel_details
from .models import Wallet, Transaction
from decimal import Decimal

@login_required
def home_view(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    context = {'wallet_balance': wallet.balance}
    return render(request, 'index.html', context)

@login_required
def wallet_view(request):
    wallet = Wallet.objects.get(user=request.user)
    transactions = Transaction.objects.filter(wallet=wallet).order_by('-timestamp')
    context = {
        'wallet': wallet,
        'transactions': transactions,
        'razorpay_key_id': os.environ.get('RAZORPAY_KEY_ID')
    }
    return render(request, 'wallet.html', context)

@login_required
def create_order_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = int(float(data.get('amount')) * 100)
            if amount < 100:
                return JsonResponse({'error': 'Amount must be at least ₹1'}, status=400)
            
            razorpay_client = razorpay.Client(auth=(os.environ.get('RAZORPAY_KEY_ID'), os.environ.get('RAZORPAY_KEY_SECRET')))
            order_data = {'amount': amount, 'currency': 'INR', 'receipt': f'receipt_{request.user.id}_{Transaction.objects.count()}'}
            order = razorpay_client.order.create(data=order_data)

            wallet = Wallet.objects.get(user=request.user)
            Transaction.objects.create(wallet=wallet, amount=Decimal(data.get('amount')), order_id=order['id'], status='Pending')
            return JsonResponse(order)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def payment_handler_view(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        try:
            payment_data = request.POST
            razorpay_payment_id = payment_data.get('razorpay_payment_id', '')
            razorpay_signature = payment_data.get('razorpay_signature', '')
            params_dict = {'razorpay_order_id': razorpay_order_id, 'razorpay_payment_id': razorpay_payment_id, 'razorpay_signature': razorpay_signature}
            
            razorpay_client = razorpay.Client(auth=(os.environ.get('RAZORPAY_KEY_ID'), os.environ.get('RAZORPAY_KEY_SECRET')))
            razorpay_client.utility.verify_payment_signature(params_dict)

            transaction = Transaction.objects.get(order_id=razorpay_order_id)
            transaction.payment_id = razorpay_payment_id
            transaction.status = 'Success'
            transaction.save()

            wallet = transaction.wallet
            wallet.balance += transaction.amount
            wallet.save()

            return redirect('wallet')
        except Exception as e:
            try:
                transaction = Transaction.objects.get(order_id=razorpay_order_id)
                transaction.status = 'Failed'
                transaction.save()
            except Transaction.DoesNotExist:
                pass
            return redirect('wallet')
    return HttpResponse("Invalid request", status=400)

@login_required
def analyze_channel_view(request):
    wallet = Wallet.objects.get(user=request.user)
    analysis_cost = Decimal('0.25')
    if wallet.balance < analysis_cost:
        return JsonResponse({'error': 'Insufficient balance. Please add funds to your wallet.'}, status=402)
    if request.method == 'POST':
        data = json.loads(request.body)
        channel_url = data.get('channel_url')
        api_key = os.environ.get('YOUTUBE_API_KEY')
        if not channel_url or not api_key:
            return JsonResponse({'error': 'Channel URL or API Key is missing'}, status=400)
        channel_data = get_channel_details(api_key, channel_url)
        if channel_data.get('error'):
            return JsonResponse(channel_data, status=400)
        wallet.balance -= analysis_cost
        wallet.save()
        channel_data['new_balance'] = wallet.balance
        return JsonResponse(channel_data)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
