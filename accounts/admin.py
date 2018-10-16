from django.contrib import admin
from .models import Profile, Subscription
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
