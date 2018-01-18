from django.contrib import admin
from .models import Storie, Query, Entity, Attachment, Comment, Reaction
from django.utils.safestring import mark_safe


@admin.register(Storie)
class AdminStorie(admin.ModelAdmin):
    list_display = ('image_html', 'url_html_entity', 'title', 'description', 'message', 'shares', 'date')
    actions = ['delete']
    # ordering = ('-fans',)
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def image_html(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> <image src="{}" /> </a>'.format(obj.fb_id, obj.attachment.media))

    image_html.short_description = 'image'

    def url_html_entity(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.entity.fb_id, obj.entity.name))

    url_html_entity.short_description = 'Page'
    url_html_entity.admin_order_field = 'entity_name'

    def description(self, obj):
        return obj.attachment.description

    description.short_description = 'Description'
    description.admin_order_field = 'attachment_description'

    def title(self, obj):
        return obj.attachment.title

    title.short_title = 'title'
    title.admin_order_field = 'attachment_title'

    def message(self, obj):
        return obj.attachment.message

    message.short_message = 'message'
    message.admin_order_field = 'attachment_message'

    # agregar cada tipo de reaccion y su conteo
    # enlace a comentarios y agregar de comentarios
    # lista de querys


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ('fb_id', 'message', 'date', 'storie')


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
