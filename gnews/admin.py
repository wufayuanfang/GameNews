from django.contrib import admin
from .models import *


# Register your models here.
class GNewsAdmin(admin.ModelAdmin):
    list_display = ['article_id', 'article_title', 'article_date', 'total_views', 'article_from']
    list_filter = ['article_date', 'article_from']
    list_display_links = ['article_id', 'article_title']
    search_fields = ['article_id', 'article_title']
    list_per_page = 18


class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'video_title', 'video_date', 'video_from']
    list_filter = ['video_date', 'video_from']
    list_display_links = ['id', 'video_title']
    search_fields = ['id', 'video_title']
    list_per_page = 18


class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ['id', 'ad_title']
    list_display_links = ['id', 'ad_title']
    search_fields = ['id', 'ad_title']
    list_per_page = 18


class MusicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'singer']
    list_display_links = ['id', 'title']
    search_fields = ['id', 'title', 'singer']
    list_per_page = 18


admin.site.register(GNews, GNewsAdmin)
admin.site.register(Image_article, )
admin.site.register(Video, VideoAdmin)
admin.site.register(News_special, )
admin.site.register(Advertising, AdvertisingAdmin)
admin.site.register(Music, MusicAdmin)
# admin.site.register(Poll, )
