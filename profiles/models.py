from django.db import models


class Query(models.Model):
    url = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    fb_id = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=500)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
