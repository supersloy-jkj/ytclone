from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shorts/', views.shorts_page, name='shorts_page'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:pk>/edit/', views.edit_video, name='edit_video'),
    path('video/<int:pk>/delete/', views.delete_video, name='delete_video'),
    path('video/<int:pk>/vote/<str:vote_type>/', views.vote_video, name='vote_video'),
    path('video/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('search/', views.search, name='search'),
    path('my-videos/', views.my_videos, name='my_videos'),
    path('video/<int:pk>/captions/add/', views.add_caption, name='add_caption'),
    path('video/<int:pk>/captions/<int:caption_pk>/delete/', views.delete_caption, name='delete_caption'),
]
