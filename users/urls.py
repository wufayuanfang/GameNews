# from django.contrib import admin
from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('setting/', views.setting, name='setting'),
    path('confirm/', views.confirm, name='confirm'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('change_code', views.change_code, name='change_code'),
    path('change_password', views.change_password, name='change_password'),
    path('orginal_editor/', views.orginal_editor, name='orginal_editor'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('upload_music/', views.upload_music, name='upload_music'),
    path('spider/', views.spider, name='spider'),
    path('my_vote/', views.my_vote, name='my_vote')

]
