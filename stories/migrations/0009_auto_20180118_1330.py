# Generated by Django 2.0 on 2018-01-18 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0008_auto_20180118_1328'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storie',
            old_name='shareds',
            new_name='shares',
        ),
    ]