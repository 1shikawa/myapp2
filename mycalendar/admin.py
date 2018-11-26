from django.contrib import admin
from .models import Schedule,LargeItem,MiddleItem
from django.contrib.auth.admin import UserAdmin

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('LargeItem', 'summary','kosu','date','totalkosu','register')  # 一覧に出したい項目
    list_display_links = ('LargeItem',)  # 修正リンクでクリックできる項目


class LargeItemAdmin(admin.ModelAdmin):
    list_display = ('id','name',)  # 一覧に出したい項目
    list_display_links = ('name',)  # 修正リンクでクリックできる項目


class MiddleItemAdmin(admin.ModelAdmin):
    list_display = ('id','name',)  # 一覧に出したい項目
    list_display_links = ('name',)  # 修正リンクでクリックできる項目


# admin.site.register(User, UserAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(LargeItem,LargeItemAdmin)
admin.site.register(MiddleItem,MiddleItemAdmin)
