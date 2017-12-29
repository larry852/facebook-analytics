from django.contrib import admin
from .models import Profile
from django.utils.safestring import mark_safe


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('url_html', 'image_html')
    actions = ['delete', 'reporter']
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def url_html(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.fb_id, obj.name))

    url_html.short_description = 'facebook'

    def image_html(self, obj):
        return mark_safe('<image src="{}" />'.format(obj.image))

    image_html.short_description = 'image'
