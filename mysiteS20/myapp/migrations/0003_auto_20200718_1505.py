# Generated by Django 3.0.6 on 2020-07-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20200616_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='stages',
            field=models.PositiveIntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='topic',
            name='category',
            field=models.CharField(default='Dev', max_length=200),
        ),
    ]
