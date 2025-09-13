from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    analysis_quota = models.IntegerField(default=10)
    
    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    analyses_used = models.IntegerField(default=0)

    def is_active(self):
        return self.end_date >= timezone.now()

    def has_quota(self):
        return self.analyses_used < self.plan.analysis_quota
        
    def __str__(self):
        return f"{self.user.username}'s Subscription"