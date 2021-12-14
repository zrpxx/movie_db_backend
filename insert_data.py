import csv
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_db.settings')

application = get_wsgi_application()

from api.models import Person, Movie, Category, MovieCategory, DirectorMovie, ActorMovie

movie_path = 'csv_data/movie_data_preprocessed.csv'
person_path = 'csv_data/person_data_preprocessed.csv'
with open(movie_path, encoding='utf-8') as movie_file, open(person_path, encoding='utf-8') as person_file:

    person_reader = csv.reader(person_file)
    movie_reader = csv.reader(movie_file)

    next(person_reader)

    PersonInsertList = []
    for row in person_reader:
        try:
            Person.objects.get(tmdb_id=row[5])
            print('Person already exists, ' + row[0])
        except Person.DoesNotExist:
            PersonInsertList.append(
                Person(
                    name=row[4],
                    gender=row[3],
                    biography=row[1],
                    birth=row[2],
                    tmdb_id=row[5],
                    place_birth=row[6]
                )
            )
            print(row.__str__())

    Person.objects.bulk_create(PersonInsertList)
    print(len(Person.objects.all()))

    # next(movie_reader)
    # for movie in movie_reader:
    #     print(movie.__str__())
    #
    #     movie = Movie.objects.update_or_create(
    #         title=movie[3],
    #         overview=movie[4],
    #         length=movie[5],
    #         score=movie[6],
    #         nickname=movie[10],
    #         status=movie[11],
    #         language=movie[12],
    #         budget=movie[13],
    #         revenue=movie[14],
    #         tmdb_id=movie[2]
    #     )
    #
    #     tags = movie[7]
    #     for tag in tags:
    #         try:
    #             tag_obj = Category.objects.get(name=tag)
    #         except Category.DoesNotExist:
    #             tag_obj = Category.objects.create(name=tag)
    #             tag_obj.save()
    #         finally:
    #             movie_category = MovieCategory.objects.create(
    #                 movie=movie,
    #                 category=tag_obj
    #             )
    #             movie_category.save()
    #
    #     director = movie[1]
    #     director_id = movie[9]
    #     if director != 'N/A':
    #         try:
    #             director_obj = Person.objects.get(tmdb_id=director_id)
    #         except Person.DoesNotExist:
    #             director_obj = Person.objects.create(
    #                 name=director,
    #                 tmdb_id=director_id
    #             )
    #             director_obj.save()
    #         finally:
    #             director_movie = DirectorMovie.objects.create(
    #                 movie=movie,
    #                 director=director_obj
    #             )
    #             director_movie.save()
    #
    #     actors = movie[0]
    #     actors_id = movie[8]
    #     for i in range(len(actors)):
    #         try:
    #             actor_obj = Person.objects.get(tmdb_id=actors_id[i])
    #         except Person.DoesNotExist:
    #             actor_obj = Person.objects.create(
    #                 name=actors[i],
    #                 tmdb_id=actors_id[i]
    #             )
    #             actor_obj.save()
    #         finally:
    #             ActorMovie.objects.create(
    #                 movie=movie,
    #                 actor=actor_obj
    #             )
