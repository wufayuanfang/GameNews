from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.


# class UserAdmin(admin.ModelAdmin):
#     list_filter = ('gender', 'address')  # 分组项
#     list_display = ('user_id', 'name', 'gender', 'email', 'address')  # 列表显示项
#     # list_display_links = ('user_id', )  #可链接到详情页项
#     list_editable = ('name', 'gender', 'email', 'address')  # 可在列表直接编辑项
#
#     fieldsets = (
#         ('基本选项', {
#             'fields': ('name', 'gender')
#         }
#          ),
#         ('可选选项', {
#             'fields': ('password', 'email', 'address'),
#             'classes': ('collapse',)
#         }
#          )
#     )


# admin.site.register(User, UserAdmin)
