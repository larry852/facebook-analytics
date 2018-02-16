from django.contrib import admin
from .models import Storie, Query, Entity, Attachment, Comment, Reaction
from django.utils.safestring import mark_safe


@admin.register(Storie)
class AdminStorie(admin.ModelAdmin):
    list_display = ('post', 'message', 'sentiment')
    actions = ['delete']
    list_display_links = None
    # ordering = ('-reaction__count', '-shares')

    def has_add_permission(self, request):
        return False

    def post(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> <image src="{}" height=100 width=130/> </a> By: <a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.fb_id, obj.attachment.media, obj.entity.fb_id, obj.entity.name))

    post.short_description = 'post'
    post.admin_order_field = 'id'

    def message(self, obj):
        return obj.attachment.message

    message.short_message = 'message'
    message.admin_order_field = 'attachment__message'


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ('url_html', 'message', 'image_html_storie', 'date')
    actions = ['delete']
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def url_html(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> Facebook </a>'.format(obj.fb_id))

    url_html.short_description = 'url'
    url_html.admin_order_field = 'storie'

    def image_html_storie(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> <image height=100 width=130 src="{}" /> </a>'.format(obj.storie.fb_id, obj.storie.attachment.media))

    image_html_storie.short_description = 'post'
    image_html_storie.admin_order_field = 'storie'


@admin.register(Query)
class AdminQuery(admin.ModelAdmin):
    list_display = ('url', 'date')


@admin.register(Entity)
class AdminEntity(admin.ModelAdmin):
    list_display = ('fb_id', 'name')


@admin.register(Reaction)
class AdminReaction(admin.ModelAdmin):
    list_display = ('type', 'count', 'storie')


@admin.register(Attachment)
class AdminAttachment(admin.ModelAdmin):
    list_display = ('title', 'description', 'message', 'media')
