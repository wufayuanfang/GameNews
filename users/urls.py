from django.urls import path

from . import views

urlpatterns = [
    # 登录注册
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('setting/', views.setting, name='setting'),
    path('confirm/', views.confirm, name='confirm'),

    # 找回密码
    path('change_pass/<str:username>/<str:code>', views.ForgotPass.as_view(), name='re_password'),
    path('change_pass/', views.ForgotPass.as_view(), name='re_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),

    path('editor/', views.editor, name="editor"),

    path('orginal_editor/', views.orginal_editor, name='orginal_editor'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('upload_music/', views.upload_music, name='upload_music'),
    path('spider/', views.spider, name='spider'),
    path('my_vote/', views.my_vote, name='my_vote'),

]
