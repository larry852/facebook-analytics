# Generated by Django 2.0 on 2018-01-18 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20180118_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.CharField(default=None, max_length=1000),
        ),
    ]
