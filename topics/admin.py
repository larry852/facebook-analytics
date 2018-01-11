from django.contrib import admin
from .models import Entity, Relation
from django.utils.safestring import mark_safe


@admin.register(Entity)
class AdminEntity(admin.ModelAdmin):
    list_display = ('image_html', 'url_html', 'type', 'fans')
    actions = ['delete']
    ordering = ('-fans',)
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def url_html(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.fb_id, obj.name))

    url_html.short_description = 'facebook'
    url_html.admin_order_field = 'name'

    def image_html(self, obj):
        return mark_safe('<image src="{}" />'.format(obj.image))

    image_html.short_description = 'image'


@admin.register(Relation)
class AdminRelation(admin.ModelAdmin):
    list_display = ('image_html_entity', 'url_html_entity', 'url_html_profile', 'image_html_profile')
    actions = ['delete']
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def url_html_entity(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.entity.fb_id, obj.entity.name))

    url_html_entity.short_description = 'Entity facebook'
    url_html_entity.admin_order_field = 'entity__name'

    def image_html_entity(self, obj):
        return mark_safe('<image src="{}" />'.format(obj.entity.image))

    image_html_entity.short_description = 'Entity image'

    def url_html_profile(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.profile.fb_id, obj.profile.name))

    url_html_profile.short_description = 'Profile facebook'
    url_html_profile.admin_order_field = 'profile__name'

    def image_html_profile(self, obj):
        return mark_safe('<image src="{}" />'.format(obj.profile.image))

    image_html_profile.short_description = 'Profile image'
