from django.contrib import admin
from .models import *


# Register your models here.

class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'dis', 'current', 'state', 'type']
    list_filter = ['state', 'dis']
    list_display_links = ['id', 'name', 'dis']
    search_fields = ['id', 'name', 'state']
    list_per_page = 40


admin.site.register(Discount, DiscountAdmin)
