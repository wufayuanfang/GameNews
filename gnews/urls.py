from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('getnews/', views.getnews, name='getnews'),
    path('news/', views.news, name='news'),
    path('video/', views.videos, name='video'),
    path('vote/', views.vote, name='vote'),
    path('getvideo/', views.getvideo, name='getvideo')

]
