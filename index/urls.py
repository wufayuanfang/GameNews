from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('music/', views.music, name='music'),

    # path('games/<str:discount>', views.GameDiscount.as_view()),

    path('search/', views.search, name='search')

]
