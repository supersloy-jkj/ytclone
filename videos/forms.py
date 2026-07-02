from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Video, Comment, Playlist, Caption


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail', 'category', 'is_short']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'video_file': _('Video file'),
            'thumbnail': _('Thumbnail'),
            'category': _('Category'),
            'is_short': _('This is a Short'),
        }


class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'thumbnail', 'category', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'thumbnail': _('Thumbnail'),
            'category': _('Category'),
            'is_published': _('Public (visible to everyone)'),
        }


class CaptionForm(forms.ModelForm):
    class Meta:
        model = Caption
        fields = ['language', 'file', 'is_default']
        labels = {
            'language': _('Language'),
            'file': _('Caption file (.vtt)'),
            'is_default': _('Set as default'),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': _('Add a comment...')}),
        }
        labels = {'content': ''}


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'is_public']
