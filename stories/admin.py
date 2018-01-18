from django.contrib import admin
from .models import Storie, Query, Entity, Attachment, Comment, Reaction


@admin.register(Storie)
class AdminStorie(admin.ModelAdmin):
    list_display = ('fb_id', 'attachment')


@admin.register(Query)
class AdminQuery(admin.ModelAdmin):
    list_display = ('url', 'date')


@admin.register(Entity)
class AdminEntity(admin.ModelAdmin):
    list_display = ('fb_id', 'name')


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ('fb_id', 'message', 'date', 'storie')


@admin.register(Reaction)
class AdminReaction(admin.ModelAdmin):
    list_display = ('type', 'count', 'storie')


@admin.register(Attachment)
class AdminAttachment(admin.ModelAdmin):
    list_display = ('title', 'description', 'message', 'media')
