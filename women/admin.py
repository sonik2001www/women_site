from django.contrib import admin
from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('content', 'title')
    list_editable = ('is_published', )
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class GameAdmin(admin.ModelAdmin):
    list_display = ('user_1', 'user_2', 'score_1', 'score_2')
    list_display_links = ('user_1', 'user_2')


class ChatAdmin(admin.ModelAdmin):
    list_display = ('user_1', 'user_2', 'time_create', 'time_update')
    list_display_links = ('user_1', 'user_2')


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GameRoom, GameAdmin)
admin.site.register(Chat, ChatAdmin)

