# Generated by Django 2.0 on 2018-01-13 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_auto_20180111_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='fb_id',
            field=models.CharField(max_length=100),
        ),
    ]
