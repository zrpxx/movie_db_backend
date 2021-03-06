# Generated by Django 3.2.5 on 2021-12-06 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('overview', models.CharField(max_length=500)),
                ('length', models.IntegerField()),
                ('score', models.FloatField(default=-1)),
                ('nickname', models.CharField(default='N/A', max_length=50)),
                ('status', models.CharField(default='N/A', max_length=50)),
                ('budget', models.IntegerField(default=-1)),
                ('revenue', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('birth', models.CharField(max_length=50)),
                ('biography', models.CharField(default='N/A', max_length=500)),
                ('place_birth', models.CharField(default='N/A', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('role', models.CharField(default='user', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MovieCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.movie')),
            ],
        ),
        migrations.CreateModel(
            name='DirectorMovie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(default='Director', max_length=50)),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.movie')),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.person')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=500)),
                ('score', models.FloatField(default=-1)),
                ('nickname', models.CharField(default='N/A', max_length=50)),
                ('status', models.CharField(default='N/A', max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.movie')),
            ],
        ),
        migrations.CreateModel(
            name='ActorMovie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(default='Starred', max_length=50)),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.movie')),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.person')),
            ],
        ),
    ]
