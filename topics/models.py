from django.db import models
from profiles.models import Profile


class Entity(models.Model):
    fb_id = models.IntegerField()
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=500)
    types_entitys = (
        ('page', 'Page of Facebook'),
        ('group', 'Group of Facebook'),
    )
    type = models.CharField(max_length=10, choices=types_entitys, default='page')


class Relation(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
