import xadmin
from .models import *

from xadmin import views


# Register your models here.

class DiscountAdmin(object):
    list_display = ['id', 'name', 'dis', 'current', 'state', 'type']
    list_filter = ['state', 'dis']
    list_display_links = ['id', 'name', 'dis']
    search_fields = ['id', 'name', 'state']
    list_per_page = 40


xadmin.site.register(Discount, DiscountAdmin)


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True  # 支持切换主题


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "xx游戏资讯后台管理系统"  # 设置站点标题
    site_footer = "xx游戏资讯xadmin后台管理系统"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠，在左侧，默认的
    # 设置models的全局图标, UserProfile, Sports 为表名
    # global_search_models = [UserProfile, Sports]
    # global_models_icon = {
    #     UserProfile: "glyphicon glyphicon-user", Sports: "fa fa-cloud"}


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
