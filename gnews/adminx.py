import xadmin
from .models import *


# Register your models here.
class GNewsAdmin(object):
    list_display = ['article_id', 'article_title', 'article_date', 'total_views', 'article_from']
    list_filter = ['article_date', 'article_from']
    list_display_links = ['article_id', 'article_title']
    search_fields = ['article_id', 'article_title']
    list_per_page = 18

    # 图标
    model_icon = 'fa fa-book'


class VideoAdmin(object):
    list_display = ['id', 'video_title', 'video_date', 'video_from']
    list_filter = ['video_date', 'video_from']
    list_display_links = ['id', 'video_title']
    search_fields = ['id', 'video_title']
    list_per_page = 18

    # 图标
    model_icon = 'fa fa-television'


class AdvertisingAdmin(object):
    list_display = ['id', 'ad_title']
    list_display_links = ['id', 'ad_title']
    search_fields = ['id', 'ad_title']
    list_per_page = 18


class MusicAdmin(object):
    list_display = ['id', 'title', 'singer']
    list_display_links = ['id', 'title']
    search_fields = ['id', 'title', 'singer']
    list_per_page = 18

    # 图标
    model_icon = 'fa fa-music'


class Image_articleAdmin(object):
    # 图标
    model_icon = 'fa fa-photo'


xadmin.site.register(GNews, GNewsAdmin)
xadmin.site.register(Image_article, Image_articleAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(News_special, )
xadmin.site.register(Advertising, AdvertisingAdmin)
xadmin.site.register(Music, MusicAdmin)
# xadmin.site.register(Poll, )
