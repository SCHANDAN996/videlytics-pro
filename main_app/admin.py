from django.contrib import admin
from .models import Wallet

# Admin panel mein Wallet model ko register karo
admin.site.register(Wallet)