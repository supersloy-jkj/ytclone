from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'subscriber_count', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('avatar', 'banner', 'bio')}),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'channel', 'subscribed_at']
