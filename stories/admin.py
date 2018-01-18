from django.contrib import admin
from .models import Storie


@admin.register(Storie)
class AdminStorie(admin.ModelAdmin):
    list_display = ('fb_id', 'attachment')
