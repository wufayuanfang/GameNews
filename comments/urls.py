from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.comment, name='comment'),
    path('comment_del/', views.comment_del, name='comment_del'),
    path('comment_video_del', views.comment_video_del, name='comment_video_del'),
    path('comment_video_post/', views.post_comment, name='comment_video_post')
]
