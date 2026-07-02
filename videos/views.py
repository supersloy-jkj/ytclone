from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import gettext as _
from .models import Video, Vote, Comment, WatchHistory, Category, Playlist, Caption
from .forms import VideoUploadForm, VideoEditForm, CommentForm, CaptionForm


def home(request):
    videos = Video.objects.filter(
        is_published=True, is_short=False
    ).select_related('uploader').order_by('-uploaded_at')
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        videos = videos.filter(category__slug=selected_category)
    return render(request, 'videos/home.html', {
        'videos': videos,
        'categories': categories,
        'selected_category': selected_category,
    })


def shorts_page(request):
    shorts = Video.objects.filter(
        is_published=True, is_short=True
    ).select_related('uploader').order_by('-uploaded_at')

    liked_ids = []
    if request.user.is_authenticated:
        liked_ids = list(
            Vote.objects.filter(
                user=request.user, vote_type='like',
                video__in=shorts
            ).values_list('video_id', flat=True)
        )
    return render(request, 'videos/shorts.html', {
        'shorts': shorts,
        'liked_ids': liked_ids,
    })


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk, is_published=True)

    Video.objects.filter(pk=pk).update(views=video.views + 1)

    if request.user.is_authenticated:
        WatchHistory.objects.update_or_create(user=request.user, video=video)

    comments = video.comments.filter(parent=None).select_related('user').prefetch_related(
        'replies__user'
    )
    related_videos = Video.objects.filter(
        is_published=True, is_short=False
    ).exclude(pk=pk).select_related('uploader')[:15]

    comment_form = CommentForm()
    user_vote = None
    is_subscribed = False

    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(user=request.user, video=video).vote_type
        except Vote.DoesNotExist:
            pass
        from users.models import Subscription
        is_subscribed = Subscription.objects.filter(
            subscriber=request.user, channel=video.uploader
        ).exists()

    return render(request, 'videos/video_detail.html', {
        'video': video,
        'comments': comments,
        'related_videos': related_videos,
        'comment_form': comment_form,
        'user_vote': user_vote,
        'is_subscribed': is_subscribed,
        'captions': video.captions.all(),
    })


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploader = request.user
            video.save()
            messages.success(request, _('Video uploaded successfully!'))
            return redirect('video_detail', pk=video.pk)
    else:
        form = VideoUploadForm()
    return render(request, 'videos/upload.html', {'form': form})


@login_required
def edit_video(request, pk):
    video = get_object_or_404(Video, pk=pk, uploader=request.user)
    if request.method == 'POST':
        form = VideoEditForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, _('Video updated!'))
            return redirect('video_detail', pk=video.pk)
    else:
        form = VideoEditForm(instance=video)
    return render(request, 'videos/edit_video.html', {
        'form': form,
        'video': video,
        'caption_form': CaptionForm(),
        'captions': video.captions.all(),
    })


@login_required
def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk, uploader=request.user)
    if request.method == 'POST':
        video.delete()
        messages.success(request, _('Video deleted.'))
        return redirect('home')
    return render(request, 'videos/delete_video.html', {'video': video})


@login_required
def vote_video(request, pk, vote_type):
    video = get_object_or_404(Video, pk=pk)
    vote, created = Vote.objects.get_or_create(
        user=request.user, video=video, defaults={'vote_type': vote_type}
    )
    if not created:
        if vote.vote_type == vote_type:
            vote.delete()
        else:
            vote.vote_type = vote_type
            vote.save()
    # Check if came from shorts
    referer = request.META.get('HTTP_REFERER', '')
    if 'shorts' in referer:
        return redirect('shorts_page')
    return redirect('video_detail', pk=pk)


@login_required
def add_comment(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    comment.parent = Comment.objects.get(pk=parent_id)
                except Comment.DoesNotExist:
                    pass
            comment.save()
    return redirect('video_detail', pk=pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    video_pk = comment.video.pk
    comment.delete()
    return redirect('video_detail', pk=video_pk)


def search(request):
    query = request.GET.get('q', '').strip()
    videos = Video.objects.none()
    if query:
        videos = Video.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_published=True
        ).select_related('uploader')
    return render(request, 'videos/search.html', {'videos': videos, 'query': query})


@login_required
def my_videos(request):
    videos = Video.objects.filter(uploader=request.user).order_by('-uploaded_at')
    return render(request, 'videos/my_videos.html', {'videos': videos})


@login_required
def add_caption(request, pk):
    """Upload a new caption/subtitle track for a video you own.

    If a caption already exists for the chosen language, its file is replaced
    instead of erroring out, since (video, language) is unique.
    """
    video = get_object_or_404(Video, pk=pk, uploader=request.user)
    if request.method == 'POST':
        form = CaptionForm(request.POST, request.FILES)
        if form.is_valid():
            new_caption = form.save(commit=False)
            existing = Caption.objects.filter(video=video, language=new_caption.language).first()
            if existing:
                existing.file = new_caption.file
                existing.is_default = new_caption.is_default
                existing.save()
                messages.success(
                    request,
                    _('Updated %(language)s captions.') % {'language': existing.get_language_display()}
                )
            else:
                new_caption.video = video
                new_caption.save()
                messages.success(
                    request,
                    _('Added %(language)s captions.') % {'language': new_caption.get_language_display()}
                )
        else:
            messages.error(request, _('Could not add captions. Please choose a language and a .vtt file.'))
    return redirect('edit_video', pk=video.pk)


@login_required
def delete_caption(request, pk, caption_pk):
    video = get_object_or_404(Video, pk=pk, uploader=request.user)
    caption = get_object_or_404(Caption, pk=caption_pk, video=video)
    if request.method == 'POST':
        caption.delete()
        messages.success(request, _('Captions removed.'))
    return redirect('edit_video', pk=video.pk)
