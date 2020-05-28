from .models import *
import xadmin


# Register your models here.
class CommentAdmin(object):
    # 显示列表的字段
    list_display = ['user', 'text', 'created_time', 'article']
    # list_filter = ['user', 'article']
    # 列表可修改字段
    list_editable = ['text']
    # 列表可点击进详情字段
    list_display_links = ['text']
    # 搜索字段
    search_fields = ['text']
    # 不可修改字段（只能是时间字段）
    readonly_fields = ('created_time',)
    list_per_page = 40

    # 图标
    model_icon = 'fa fa-comment-o'


class Comment_videoAdmin(object):
    list_display = ('id', 'user', 'video', 'text', 'parent', 'level')
    list_display_links = ['text']
    # 列表可修改字段
    list_editable = ['text']
    # 图标
    model_icon = 'fa fa-comments-o'


xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Comment_vidoe, Comment_videoAdmin)
