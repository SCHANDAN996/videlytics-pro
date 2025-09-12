from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Wallet

# Yeh signal tab chalega jab naya User banega
@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

# Yeh signal tab chalega jab User save hoga
@receiver(post_save, sender=User)
def save_wallet(sender, instance, **kwargs):
    try:
        instance.wallet.save()
    except AttributeError:
        # Agar kisi purane user ka wallet nahi bana hai, to bana do
        Wallet.objects.create(user=instance)