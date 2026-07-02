from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Subscription
from .forms import RegisterForm, EditProfileForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def channel(request, username):
    channel_user = get_object_or_404(CustomUser, username=username)
    videos = channel_user.videos.filter(is_published=True).order_by('-uploaded_at')
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(
            subscriber=request.user, channel=channel_user
        ).exists()
    return render(request, 'users/channel.html', {
        'channel_user': channel_user,
        'videos': videos,
        'is_subscribed': is_subscribed,
    })


@login_required
def toggle_subscription(request, username):
    channel_user = get_object_or_404(CustomUser, username=username)
    if channel_user == request.user:
        messages.error(request, "You can't subscribe to your own channel.")
        return redirect('channel', username=username)

    sub, created = Subscription.objects.get_or_create(
        subscriber=request.user, channel=channel_user
    )
    if not created:
        sub.delete()
        messages.info(request, f'Unsubscribed from {channel_user.username}.')
    else:
        messages.success(request, f'Subscribed to {channel_user.username}!')
    return redirect('channel', username=username)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('channel', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def watch_history(request):
    history = request.user.watchhistory_set.select_related('video__uploader').all()
    return render(request, 'users/history.html', {'history': history})


@login_required
def subscriptions_feed(request):
    subscribed_channels = request.user.subscriptions.values_list('channel', flat=True)
    from videos.models import Video
    videos = Video.objects.filter(
        uploader__in=subscribed_channels, is_published=True
    ).order_by('-uploaded_at')
    return render(request, 'users/subscriptions.html', {'videos': videos})
