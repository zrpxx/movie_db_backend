# Generated by Django 3.2.5 on 2021-12-06 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_person_biography'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='tmdb_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='tmdb_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
