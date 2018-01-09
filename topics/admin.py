from django.contrib import admin
from .models import Entity, Relation


@admin.register(Entity)
class AdminEntity(admin.ModelAdmin):
    list_display = ('fb_id', 'name', 'image', 'type')
    actions = ['delete']
    list_display_links = None

    def has_add_permission(self, request):
        return False


@admin.register(Relation)
class AdminRelation(admin.ModelAdmin):
    list_display = ('entity', 'profile')
    actions = ['delete']
    list_display_links = None

    def has_add_permission(self, request):
        return False
