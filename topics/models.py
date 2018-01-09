from django.db import models
from profiles.models import Profile


class Page(models.Model):
    fb_id = models.IntegerField()
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=500)


class Like(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
