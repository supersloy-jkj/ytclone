from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('history/', views.watch_history, name='watch_history'),
    path('subscriptions/', views.subscriptions_feed, name='subscriptions_feed'),
    path('channel/<str:username>/', views.channel, name='channel'),
    path('channel/<str:username>/subscribe/', views.toggle_subscription, name='toggle_subscription'),
]
