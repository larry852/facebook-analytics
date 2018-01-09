from django.contrib import admin
from .models import Profile, Query
from django.utils.safestring import mark_safe
from topics import utils as topics_utils


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('url_html', 'image_html', 'get_query_html', 'get_date')
    actions = ['delete', 'topics']
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

    def get_query_html(self, obj):
        querys = obj.query.url.split('/')
        html = ''
        for query in querys:
            if query:
                html += '<li> {} </li>'.format(query)
        return mark_safe(html)

    get_query_html.short_description = 'query'
    get_query_html.admin_order_field = 'query__url'

    def get_date(self, obj):
        return obj.query.date

    get_date.short_description = 'date'
    get_date.admin_order_field = 'query__date'

    def topics(self, request, queryset):
        return topics_utils.generate(queryset)

    topics.short_description = "Get topics"


@admin.register(Query)
class QueryProfile(admin.ModelAdmin):
    list_display = ('url_html', 'date')
    actions = ['delete', 'reporter']
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def url_html(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.url, obj.url))

    url_html.short_description = 'query'
    url_html.admin_order_field = 'url'
