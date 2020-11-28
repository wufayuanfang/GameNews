from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.Discuss.as_view(), name='comments'),
    path('comment_video_del', views.comment_video_del, name='comment_video_del'),
    path('comment_video_post/', views.post_comment, name='comment_video_post')
]
