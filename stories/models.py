from django.db import models


class Query(models.Model):
    url = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)


class Entity(models.Model):
    fb_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=1000, default=None, null=True)


class Attachment(models.Model):
    title = models.CharField(max_length=500, default=None, null=True)
    description = models.CharField(max_length=5000, default=None, null=True)
    message = models.CharField(max_length=5000, default=None, null=True)
    media = models.CharField(max_length=1000)


class Storie(models.Model):
    fb_id = models.CharField(max_length=1000)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True)
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    date = models.DateTimeField()
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    shares = models.IntegerField(default=0)
    sentiment = models.DecimalField(default=0, max_digits=30, decimal_places=15)


class Comment(models.Model):
    fb_id = models.CharField(max_length=1000)
    message = models.CharField(max_length=5000)
    date = models.DateTimeField()
    image = models.CharField(max_length=1000, default=None, null=True)
    storie = models.ForeignKey(Storie, on_delete=models.CASCADE)


class Reaction(models.Model):
    types_entitys = (
        ('NONE', 'NONE'),
        ('LIKE', 'LIKE'),
        ('LOVE', 'LOVE'),
        ('WOW', 'WOW'),
        ('HAHA', 'HAHA'),
        ('SAD', 'SAD'),
        ('ANGRY', 'ANGRY'),
        ('THANKFUL', 'THANKFUL'),
    )
    type = models.CharField(max_length=10, choices=types_entitys, default='NONE')
    count = models.IntegerField(default=0)
    storie = models.ForeignKey(Storie, on_delete=models.CASCADE)
