# Generated by Django 3.2.5 on 2021-12-06 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='biography',
            field=models.CharField(default='N/A', max_length=5000),
        ),
    ]
