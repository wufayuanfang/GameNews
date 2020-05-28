from django.contrib import admin
from .models import *


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    # list_display = ['user', 'created_time', 'article']
    # list_filter = ['user', 'article']
    # list_display_links = ['user', 'article']
    search_fields = ['text']
    list_per_page = 40


class Comment_videoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'text', 'parent', 'level')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Comment_vidoe, Comment_videoAdmin)