from django.contrib import admin
from .models import Video, Category, Vote, Comment, WatchHistory, Playlist, Caption


class CaptionInline(admin.TabularInline):
    model = Caption
    extra = 0


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploader', 'views', 'like_count', 'is_published', 'uploaded_at']
    list_filter = ['is_published', 'category', 'uploaded_at']
    search_fields = ['title', 'description', 'uploader__username']
    list_editable = ['is_published']
    inlines = [CaptionInline]


@admin.register(Caption)
class CaptionAdmin(admin.ModelAdmin):
    list_display = ['video', 'language', 'is_default', 'uploaded_at']
    list_filter = ['language', 'is_default']
    search_fields = ['video__title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'vote_type']


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'watched_at']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'is_public', 'created_at']
