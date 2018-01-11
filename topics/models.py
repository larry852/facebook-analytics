from django.db import models
from profiles.models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Entity(models.Model):
    fb_id = models.IntegerField()
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=500)
    types_entitys = (
        ('page', 'Page of Facebook'),
        ('group', 'Group of Facebook'),
    )
    type = models.CharField(max_length=10, choices=types_entitys, default='page')
    fans = models.IntegerField(default=0, editable=False)


class Relation(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


@receiver([post_delete, post_save], sender=Relation)
def count_fan(sender, **kwargs):
    for entity in Entity.objects.all():
        count = Relation.objects.filter(entity=entity).count()
        entity.fans = count
        entity.save()
