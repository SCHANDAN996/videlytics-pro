from django.contrib import admin
from .models import Plan, UserProfile, Subscription

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'razorpay_plan_id')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'referral_code', 'referral_credits', 'referred_by')
    search_fields = ('user__username',)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan', 'is_active')
    search_fields = ('user__username',)

admin.site.register(Plan, PlanAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
