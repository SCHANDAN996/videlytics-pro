from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import SubscriptionPlan, UserSubscription
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender=User)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        try:
            free_plan, created_plan = SubscriptionPlan.objects.get_or_create(
                name='Free', 
                defaults={'price': 0, 'analysis_quota': 10}
            )
            UserSubscription.objects.create(
                user=instance,
                plan=free_plan,
                end_date=timezone.now() + timedelta(days=3650) # Free plan 10 saal ke liye
            )
        except Exception as e:
            print(f"WARNING: Could not create free subscription for {instance.username}. Error: {e}")