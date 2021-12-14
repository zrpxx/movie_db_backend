import csv
import json
import os
import pickle

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_db.settings')

application = get_wsgi_application()

from api.models import Person, Movie, Category, MovieCategory, DirectorMovie, ActorMovie

movie_path = 'csv_data/movie_data_preprocessed.csv'
person_path = 'csv_data/person_data_preprocessed.csv'
with open(movie_path, encoding='utf-8') as movie_file, open(person_path, encoding='utf-8') as person_file:
    person_reader = csv.reader(person_file)
    movie_reader = csv.reader(movie_file)

    #    next(person_reader)

    # for row in person_reader:
    #     Person.objects.update_or_create(
    #         name=row[4],
    #         gender=row[3],
    #         biography=row[1],
    #         birth=row[2],
    #         tmdb_id=row[5],
    #         place_birth=row[6]
    #     )
    #     print(row.__str__())
    #     print(len(Person.objects.all()))

    # next(movie_reader)
    # MovieInsertList = []
    # for movie in movie_reader:
    #     print(movie.__str__())
    #     try:
    #         movie_obj = Movie.objects.get(tmdb_id=movie[2])
    #         print("Movie already exists")
    #     except Movie.DoesNotExist:
    #         movie_obj = Movie(
    #             title=movie[3],
    #             overview=movie[4],
    #             length=movie[5],
    #             score=movie[6],
    #             nickname=movie[10],
    #             status=movie[11],
    #             language=movie[12],
    #             budget=float(movie[13]) if movie[13] else -1,
    #             revenue=float(movie[14]) if movie[14] else -1,
    #             tmdb_id=movie[2]
    #         )
    #         MovieInsertList.append(movie_obj)
    #         print("Movie added, total: " + str(len(MovieInsertList)))
    # Movie.objects.bulk_create(MovieInsertList)

    movie_reader = csv.reader(movie_file)
    next(movie_reader)
    TagList = []
    DirectorList = []
    ActorList = []

    for movie in movie_reader:
        try:
            movie_obj = Movie.objects.get(tmdb_id=movie[2])
            print("Processing movie: " + movie_obj.id.__str__())

            tags = eval(movie[7])
            for tag in tags:
                print("Tag: " + tag)
                try:
                    tag_obj = Category.objects.get(name=tag)
                except Category.DoesNotExist:
                    tag_obj = Category.objects.create(name=tag)
                    tag_obj.save()
                finally:
                    TagList.append(
                        MovieCategory(
                            movie_id=movie_obj,
                            category_id=tag_obj
                        )
                    )

            director = movie[1]
            print('Director: ' + director)
            director_id = movie[9]
            if director != 'N/A':
                try:
                    director_obj = Person.objects.get(tmdb_id=director_id)

                    DirectorList.append(
                        DirectorMovie(
                            movie_id=movie_obj,
                            person_id=director_obj
                        )
                    )

                    actors = eval(movie[0])
                    print('Actors: ' + actors.__str__())
                    actors_id = eval(movie[8])
                    if len(actors) > 0:
                        for i in range(len(actors)):
                            if actors[i] == '':
                                continue
                            try:
                                actor_obj = Person.objects.get(tmdb_id=int(actors_id[i]))
                                ActorList.append(
                                    ActorMovie(
                                        movie_id=movie_obj,
                                        person_id=actor_obj
                                    )
                                )
                            except Person.DoesNotExist:
                                continue
                            except:
                                continue
                    print("Added", movie_obj.title)
                except Person.DoesNotExist:
                    actors = eval(movie[0])
                    print('Actors: ' + actors.__str__())
                    actors_id = eval(movie[8])
                    if len(actors) > 0:
                        for i in range(len(actors)):
                            if actors[i] == '':
                                continue
                            try:
                                actor_obj = Person.objects.get(tmdb_id=int(actors_id[i]))
                                ActorList.append(
                                    ActorMovie(
                                        movie_id=movie_obj,
                                        person_id=actor_obj
                                    )
                                )
                            except Person.DoesNotExist:
                                continue
                            except:
                                continue
                    print("Added", movie_obj.title)
            else:
                actors = eval(movie[0])
                print('Actors: ' + actors.__str__())
                actors_id = eval(movie[8])
                if len(actors) > 0:
                    for i in range(len(actors)):
                        if actors[i] == '':
                            continue
                        try:
                            actor_obj = Person.objects.get(tmdb_id=int(actors_id[i]))
                            ActorList.append(
                                ActorMovie(
                                    movie_id=movie_obj,
                                    person_id=actor_obj
                                )
                            )
                        except Person.DoesNotExist:
                            continue
                        except:
                            continue
                print("Added", movie_obj.title)
        except:
            continue

    MovieCategory.objects.bulk_create(TagList)
    print("MovieCategory added, total: " + str(len(TagList)))
    DirectorMovie.objects.bulk_create(DirectorList)
    print("DirectorMovie added, total: " + str(len(DirectorList)))
    ActorMovie.objects.bulk_create(ActorList)
    print("ActorMovie added, total: " + str(len(ActorList)))
