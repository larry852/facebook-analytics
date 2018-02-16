from django.contrib import admin
from .models import Storie, Query, Entity, Attachment, Comment, Reaction
from django.utils.safestring import mark_safe


@admin.register(Storie)
class AdminStorie(admin.ModelAdmin):
    list_display = ('post', 'message', 'range_sentiment_post', 'range_sentiment_comment', 'count_sentiment_comment')
    actions = ['delete']
    list_display_links = None
    ordering = ('-sentiment',)

    def has_add_permission(self, request):
        return False

    def post(self, obj):
        return mark_safe('<a target="_blank" href="https://www.facebook.com/{}"> <image src="{}" height=100 width=130/> </a> By: <a target="_blank" href="https://www.facebook.com/{}"> {} </a>'.format(obj.fb_id, obj.attachment.media, obj.entity.fb_id, obj.entity.name))

    def message(self, obj):
        return obj.attachment.message

    def range_sentiment_post(self, obj):
        score = round(obj.sentiment, 2)
        if -1 <= score <= -0.25:
            return mark_safe('<span style="background-color: #e53935;color: #fff;">{} / {}</span>'.format('Negative', score))
        elif 0.25 <= score <= 1:
            return mark_safe('<span style="background-color: #388e3c;color: #fff;">{} / {}</span>'.format('Positive', score))
        else:
            return mark_safe('<span style="background-color: #ffe57f;">{} / {}</span>'.format('Neutral', score))

    range_sentiment_post.admin_order_field = 'sentiment'

    def range_sentiment_comment(self, obj):
        score = 0
        comments = Comment.objects.filter(storie=obj)
        if comments:
            for comment in comments:
                score += comment.sentiment
            score = score / len(comments)
            score = round(obj.sentiment, 2)
            if -1 <= score <= -0.25:
                return mark_safe('<span style="background-color: #e53935;color: #fff;">{} / {}</span>'.format('Negative', score, obj.id))
            elif 0.25 <= score <= 1:
                return mark_safe('<span style="background-color: #388e3c;color: #fff;">{} / {}</span>'.format('Positive', score, obj.id))
            else:
                return mark_safe('<span style="background-color: #ffe57f;">{} / {}</span>'.format('Neutral', score, obj.id))
        return "No comments"

    def count_sentiment_comment(self, obj):
        positive = 0
        neutral = 0
        negative = 0
        comments = Comment.objects.filter(storie=obj)
        if comments:
            for comment in comments:
                score = round(comment.sentiment, 2)
                if -1 <= score <= -0.25:
                    negative += 1
                elif 0.25 <= score <= 1:
                    positive += 1
                else:
                    neutral += 1
            return mark_safe('Positive: {}/{total} <br> Neutral: {}/{total} <br> Negative: {}/{total} <br><br><a target="_blank" href="/admin/stories/comment/?storie__id__exact={}">List comments</a>'.format(positive, neutral, negative, obj.id, total=len(comments)))
        return "No comments"


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ('url_html', 'message', 'image_html_storie', 'range_sentiment_comment')
    list_filter = ('storie', )
    actions = ['delete']
    list_display_links = None
    ordering = ('-storie', '-sentiment')

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

    def range_sentiment_comment(self, obj):
        score = round(obj.sentiment, 2)
        if -1 <= score <= -0.25:
            return mark_safe('<span style="background-color: #e53935;color: #fff;">{} / {}</span>'.format('Negative', score))
        elif 0.25 <= score <= 1:
            return mark_safe('<span style="background-color: #388e3c;color: #fff;">{} / {}</span>'.format('Positive', score))
        else:
            return mark_safe('<span style="background-color: #ffe57f;">{} / {}</span>'.format('Neutral', score))


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
