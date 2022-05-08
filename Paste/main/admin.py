from django.contrib import admin
from main.models import *

# Register your models here.

class PasteAdmin(admin.ModelAdmin):
    list_display = ('title','time', )
    list_display_links = ('title', )

admin.site.register(Paste, PasteAdmin)

@admin.action(description="Enable")
def enable(modeladmin, request, queryset):
    queryset.update(enabled=True)

@admin.action(description="Disable")
def disable(modeladmin, request, queryset):
    queryset.update(enabled=False)

class BanAdmin(admin.ModelAdmin):
    list_display = ('keyword','enabled', )
    list_display_links = ('keyword', )
    actions = (enable,disable)

admin.site.register(Ban, BanAdmin)

