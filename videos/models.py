from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    views = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    is_short = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.votes.filter(vote_type='like').count()

    @property
    def dislike_count(self):
        return self.votes.filter(vote_type='dislike').count()

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def has_captions(self):
        return self.captions.exists()


class Caption(models.Model):
    """A closed-caption / subtitle track (.vtt) attached to a video, in a given language."""

    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('es', _('Spanish')),
        ('fr', _('French')),
        ('de', _('German')),
        ('pt', _('Portuguese')),
        ('hi', _('Hindi')),
        ('ar', _('Arabic')),
        ('zh', _('Chinese')),
        ('ja', _('Japanese')),
        ('ko', _('Korean')),
        ('ru', _('Russian')),
        ('it', _('Italian')),
        ('tr', _('Turkish')),
        ('vi', _('Vietnamese')),
        ('id', _('Indonesian')),
        ('bn', _('Bengali')),
        ('ur', _('Urdu')),
        ('nl', _('Dutch')),
        ('pl', _('Polish')),
        ('th', _('Thai')),
    ]

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='captions')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    file = models.FileField(
        upload_to='captions/',
        validators=[FileExtensionValidator(allowed_extensions=['vtt'])],
        help_text=_('WebVTT (.vtt) file.'),
    )
    is_default = models.BooleanField(default=False, help_text=_('Show this language first in the captions menu.'))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'language')
        ordering = ['-is_default', 'language']

    def __str__(self):
        return f"{self.video.title} \u2014 {self.get_language_display()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_default:
            Caption.objects.filter(video=self.video).exclude(pk=self.pk).update(is_default=False)


class Vote(models.Model):
    VOTE_TYPES = [('like', 'Like'), ('dislike', 'Dislike')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)

    class Meta:
        unique_together = ('user', 'video')


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"


class WatchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video')
        ordering = ['-watched_at']


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists'
    )
    videos = models.ManyToManyField(Video, blank=True, related_name='playlists')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
