# Generated by Django 3.2.5 on 2021-12-07 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_movie_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='tmdb_id',
            field=models.BigIntegerField(),
        ),
    ]
