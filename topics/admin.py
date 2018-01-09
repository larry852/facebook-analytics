from django.contrib import admin
from .models import Entity, Relation
from django.utils.safestring import mark_safe


@admin.register(Entity)
class AdminEntity(admin.ModelAdmin):
    list_display = ('url_html', 'image_html', 'type', 'get_count_fans')
    actions = ['delete']
    list_display_links = None

    def url_html(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.fb_id, obj.name))

    url_html.short_description = 'facebook'
    url_html.admin_order_field = 'name'

    def image_html(self, obj):
        return mark_safe('<image src="{}" />'.format(obj.image))

    image_html.short_description = 'image'

    def get_count_fans(self, obj):
        return Relation.objects.filter(entity=obj).count()

    get_count_fans.short_description = 'Fans'

    def has_add_permission(self, request):
        return False


@admin.register(Relation)
class AdminRelation(admin.ModelAdmin):
    list_display = ('entity', 'profile')
    actions = ['delete']
    list_display_links = None

    def has_add_permission(self, request):
        return False
