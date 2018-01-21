from django.contrib import admin
from .models import Storie, Query, Entity, Attachment, Comment, Reaction
from django.utils.safestring import mark_safe


@admin.register(Storie)
class AdminStorie(admin.ModelAdmin):
    list_display = ('image_html', 'url_html_entity', 'description', 'message', 'reaction_total', 'reaction_like', 'reaction_love', 'reaction_wow', 'reaction_haha', 'reaction_sad', 'reaction_angry', 'reaction_thankful', 'shares', 'date', 'get_query_html')
    actions = ['delete']
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def image_html(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> <image src="{}" height=100 width=130/> </a>'.format(obj.fb_id, obj.attachment.media))

    image_html.short_description = 'post'

    def url_html_entity(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.entity.fb_id, obj.entity.name))

    url_html_entity.short_description = 'page'
    url_html_entity.admin_order_field = 'entity'

    def description(self, obj):
        return obj.attachment.description

    description.short_description = 'description'
    description.admin_order_field = 'attachment'

    def message(self, obj):
        return obj.attachment.message

    message.short_message = 'message'
    message.admin_order_field = 'attachment'

    def reaction_haha(self, obj):
        return Reaction.objects.get(storie=obj, type='HAHA').count

    reaction_haha.admin_order_field = 'reaction'

    def reaction_total(self, obj):
        return Reaction.objects.get(storie=obj, type='NONE').count

    reaction_total.admin_order_field = 'reaction'

    def reaction_like(self, obj):
        return Reaction.objects.get(storie=obj, type='LIKE').count

    reaction_like.admin_order_field = 'reaction'

    def reaction_love(self, obj):
        return Reaction.objects.get(storie=obj, type='LOVE').count

    reaction_love.admin_order_field = 'reaction'

    def reaction_wow(self, obj):
        return Reaction.objects.get(storie=obj, type='WOW').count

    reaction_wow.admin_order_field = 'reaction'

    def reaction_sad(self, obj):
        return Reaction.objects.get(storie=obj, type='SAD').count

    reaction_sad.admin_order_field = 'reaction'

    def reaction_angry(self, obj):
        return Reaction.objects.get(storie=obj, type='ANGRY').count

    reaction_angry.admin_order_field = 'reaction'

    def reaction_thankful(self, obj):
        return Reaction.objects.get(storie=obj, type='THANKFUL').count

    reaction_thankful.admin_order_field = 'reaction'

    def get_query_html(self, obj):
        querys = obj.query.url.split('/')
        html = ''
        for query in querys:
            if query:
                html += '<li> {} </li>'.format(query)
        return mark_safe(html)

    get_query_html.short_description = 'query'
    get_query_html.admin_order_field = 'query__url'


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
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> <image src="{}" /> </a>'.format(obj.storie.fb_id, obj.storie.attachment.media))

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
