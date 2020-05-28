from django.contrib import admin
from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('music/', views.music, name='music'),
    path('discount_all/', views.discount_all, name='discount_all'),
    path('discount_steam/', views.discount_steam, name='discount_steam'),
    path('discount_switch/', views.discount_switch, name='discount_switch'),
    path('discount_ps/', views.discount_ps, name='discount_ps'),
    path('discount_xbox/', views.discount_xbox, name='discount_xbox'),
    path('search/', views.search, name='search')

]
