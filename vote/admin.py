from vote.models import *
from django.contrib import admin

class ItemAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('name', 'category', 'vote_count')

admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
