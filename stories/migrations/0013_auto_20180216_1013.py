# Generated by Django 2.0 on 2018-02-16 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0012_storie_sentiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storie',
            name='sentiment',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
        ),
    ]
