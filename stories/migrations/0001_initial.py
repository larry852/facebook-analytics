# Generated by Django 2.0 on 2018-01-18 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=5000)),
                ('media', models.CharField(max_length=1000)),
                ('type', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1000)),
                ('image', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('NONE', 'NONE'), ('LIKE', 'LIKE'), ('LOVE', 'LOVE'), ('WOW', 'WOW'), ('HAHA', 'HAHA'), ('SAD', 'SAD'), ('ANGRY', 'ANGRY'), ('THANKFUL', 'THANKFUL')], default='NONE', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Storie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_id', models.CharField(max_length=1000)),
                ('date', models.DateTimeField()),
                ('likes', models.IntegerField(default=0)),
                ('shareds', models.IntegerField(default=0)),
                ('attachment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.Attachment')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.Entity')),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.Query')),
            ],
        ),
        migrations.AddField(
            model_name='reaction',
            name='storie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.Storie'),
        ),
        migrations.AddField(
            model_name='comment',
            name='storie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.Storie'),
        ),
    ]
