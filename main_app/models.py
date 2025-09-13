from django.db import models
from django.contrib.auth.models import User
import uuid

# Plan model to store subscription plans
class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(help_text="Enter features separated by commas")
    razorpay_plan_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_features_list(self):
        return [feature.strip() for feature in self.features.split(',')]

# UserProfile to extend the default User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    referral_code = models.CharField(max_length=12, unique=True, blank=True)
    referral_credits = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_users')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4()).replace('-', '')[:10].upper()
        super().save(*args, **kwargs)

# Subscription model to track user subscriptions
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    razorpay_subscription_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.user.username}'s subscription to {self.plan.name}"
