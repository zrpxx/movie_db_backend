from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True)
    role = models.CharField(max_length=50, default='user')


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth = models.CharField(max_length=50)
    tmdb_id = models.BigIntegerField()
    biography = models.CharField(max_length=5000, default='N/A')
    place_birth = models.CharField(max_length=500, default='N/A')


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, default='N/A')


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    overview = models.CharField(max_length=5000, default='No overview')
    length = models.CharField(max_length=500, default='N/A')
    score = models.FloatField(default=-1)
    tmdb_id = models.BigIntegerField()
    language = models.CharField(max_length=50, default='N/A')
    nickname = models.CharField(max_length=500, default='N/A')
    status = models.CharField(max_length=50, default='N/A')
    budget = models.IntegerField(default=-1)
    revenue = models.IntegerField(default=-1)
    categories = models.ManyToManyField(Category, through='MovieCategory')
    actors = models.ManyToManyField(Person, through='ActorMovie', related_name='actors')
    directors = models.ManyToManyField(Person, through='DirectorMovie', related_name='directors')


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    score = models.FloatField(
        default=-1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    date = models.DateTimeField(auto_now_add=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class MovieCategory(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class ActorMovie(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='actor')
    role = models.CharField(max_length=50, default='Starred')


class DirectorMovie(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='director')
    role = models.CharField(max_length=50, default='Director')
