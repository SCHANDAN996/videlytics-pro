from django.db import models
from django.contrib.auth.models import User
import uuid

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(help_text="Comma-separated list of features.")
    razorpay_plan_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    referral_code = models.CharField(max_length=12, blank=True, unique=True)
    referral_credits = models.IntegerField(default=0)
    
    # === यह नया फ़ील्ड जोड़ा गया है ताकि एरर ठीक हो सके ===
    # यह उस यूज़र को ट्रैक करेगा जिसने इस यूज़र को रेफर किया है।
    referred_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='referrals'
    )
    # =======================================================

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    razorpay_subscription_id = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s subscription to {self.plan.name}"
