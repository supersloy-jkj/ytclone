from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)

    @property
    def subscriber_count(self):
        return self.subscribers.count()

    def __str__(self):
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='subscriptions'
    )
    channel = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='subscribers'
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'channel')

    def __str__(self):
        return f"{self.subscriber} → {self.channel}"
