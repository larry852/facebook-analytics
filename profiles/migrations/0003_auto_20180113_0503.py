# Generated by Django 2.0 on 2018-01-13 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20171229_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fb_id',
            field=models.CharField(max_length=1000),
        ),
    ]
