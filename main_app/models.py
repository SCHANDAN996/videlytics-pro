from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    # Har user ka ek hi wallet hoga
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Balance, jismein 2 decimal places tak honge
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10.00) # Naye user ko ₹10 free milenge

    def __str__(self):
        return f"{self.user.username}'s Wallet"