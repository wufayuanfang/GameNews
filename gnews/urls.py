from django.urls import path

from . import views

urlpatterns = [

    path('article/', views.Article.as_view(), name='getnews'),
    path('article/<int:pk>', views.Article.as_view(), name='getnews'),
    path('vote/', views.vote, name='vote'),
    path('video/', views.Video.as_view(), name='getvideo'),
    path('video/<int:pk>', views.Video.as_view(), name='getvideo'),

]
