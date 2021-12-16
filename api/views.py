import json
import random

from django.db.models import Max
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .models import Movie, Comment, User, Person, MovieCategory, Category
from .serializers import MovieSerializer, CommentSerializer, PersonSerializer, \
    CategorySerializer, ActorMovie, DirectorMovie


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = Movie.objects.all()
        queryset = queryset.prefetch_related('actors')
        queryset = queryset.prefetch_related('directors')
        queryset = queryset.prefetch_related('categories')
        movie_id = self.request.query_params.get('id', None)
        movie_category_ids = self.request.query_params.getlist('category_id[]', None)
        if movie_id is not None:
            queryset = queryset.filter(id=movie_id)
        if movie_category_ids is not None:
            print(movie_category_ids)
            for movie_category_id in movie_category_ids:
                queryset = queryset.filter(categories__id=movie_category_id)
        return queryset

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        actors = data.get('actors', None)
        directors = data.get('directors', None)
        categories = data.get('categories', None)

        serializer = MovieSerializer(data=data)

        if serializer.is_valid():
            movie = serializer.save()
            if actors is not None:
                data['actors'] = actors
                for actor in actors:
                    actor_id = Person.objects.filter(id=actor).first()
                    if actor_id is not None:
                        actor_movie = ActorMovie(person_id=actor_id, movie_id=movie)
                        actor_movie.save()
                    else:
                        raise Exception('Actor id is invalid')

            if directors is not None:
                data['directors'] = directors
                for director in directors:
                    director_id = Person.objects.filter(id=director).first()
                    if director_id is not None:
                        director_movie = DirectorMovie(person_id=director_id, movie_id=movie)
                        director_movie.save()
                    else:
                        raise Exception('Director id is invalid')

            if categories is not None:
                data['categories'] = categories
                for category in categories:
                    category_id = Category.objects.filter(id=category).first()
                    if category_id is not None:
                        category_movie = MovieCategory(category_id=category_id, movie_id=movie)
                        category_movie.save()
                    else:
                        raise Exception('Category id is invalid')
            return HttpResponse(status=201)
        else:
            raise Exception(serializer.errors)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        movie_id = self.request.query_params.get('id', None)
        actors = data.get('actors', None)
        directors = data.get('directors', None)
        categories = data.get('categories', None)

        if movie_id is not None:
            movie = Movie.objects.get(id=movie_id)
            serializer = MovieSerializer(movie, data=data)

            MovieCategory.objects.filter(movie_id=movie).delete()
            ActorMovie.objects.filter(movie_id=movie).delete()
            DirectorMovie.objects.filter(movie_id=movie).delete()

            if serializer.is_valid():
                serializer.save()

                if actors is not None:
                    data['actors'] = actors
                    for actor in actors:
                        actor_id = Person.objects.filter(id=actor).first()
                        if actor_id is not None:
                            actor_movie = ActorMovie(person_id=actor_id, movie_id=movie)
                            actor_movie.save()
                        else:
                            raise Exception('Actor id is invalid')

                if directors is not None:
                    data['directors'] = directors
                    for director in directors:
                        director_id = Person.objects.filter(id=director).first()
                        if director_id is not None:
                            director_movie = DirectorMovie(person_id=director_id, movie_id=movie)
                            director_movie.save()
                        else:
                            raise Exception('Director id is invalid')

                if categories is not None:
                    data['categories'] = categories
                    for category in categories:
                        category_id = Category.objects.filter(id=category).first()
                        if category_id is not None:
                            category_movie = MovieCategory(category_id=category_id, movie_id=movie)
                            category_movie.save()
                        else:
                            raise Exception('Category id is invalid')
                return HttpResponse(status=200)
            else:
                raise Exception(serializer.errors)
        else:
            raise Exception('Movie id is required')

    def delete(self, request, *args, **kwargs):
        movie_id = self.request.query_params.get('id', None)
        if movie_id is not None:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return HttpResponse(status=200)
        else:
            raise Exception('Movie id is required')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None and movie_id is not None:
            user = User.objects.filter(id=user_id).first()
            movie = Movie.objects.filter(id=movie_id).first()
            if user is not None and movie is not None:
                queryset = Comment.objects.filter(user_id=user, movie_id=movie)
            else:
                raise Exception('User id or Movie id is invalid')
        elif movie_id is not None:
            if movie_id is not None:
                movie = MovieViewSet.queryset.filter(id=movie_id).first()
                if movie is not None:
                    queryset = Comment.objects.filter(movie_id=movie)
                else:
                    raise Exception('Movie not found')
            else:
                queryset = Comment.objects.all()
        elif user_id is not None:
            if user_id is not None:
                user = User.objects.filter(id=user_id).first()
                if user is not None:
                    queryset = Comment.objects.filter(user_id=user)
                else:
                    raise Exception('User not found')
        return queryset

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        else:
            raise Exception(serializer.errors)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        comment_id = self.request.query_params.get('id', None)
        if comment_id is not None:
            comment = Comment.objects.get(id=comment_id)
            serializer = CommentSerializer(comment, data=data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(status=200)
            else:
                raise Exception(serializer.errors)
        else:
            raise Exception('Comment id is required')

    def delete(self, request, *args, **kwargs):
        comment_id = self.request.query_params.get('id', None)
        if comment_id is not None:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return HttpResponse(status=200)
        else:
            raise Exception('Comment id is required')


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def get_queryset(self):
        queryset = Person.objects.all()
        person_id = self.request.query_params.get('id', None)
        if person_id is not None:
            queryset = queryset.filter(id=person_id)
        return queryset

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        else:
            raise Exception(serializer.errors)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        person_id = self.request.query_params.get('id', None)
        if person_id is not None:
            person = Person.objects.get(id=person_id)
            serializer = PersonSerializer(person, data=data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(status=200)
            else:
                raise Exception(serializer.errors)
        else:
            raise Exception('Person id is required')

    def delete(self, request, *args, **kwargs):
        person_id = self.request.query_params.get('id', None)
        if person_id is not None:
            person = Person.objects.get(id=person_id)
            person.delete()
            return HttpResponse(status=200)
        else:
            raise Exception('Person id is required')


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        category = self.request.query_params.get('id', None)
        if category is not None:
            queryset = Category.objects.filter(category=category)
        else:
            queryset = Category.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        else:
            raise Exception(serializer.errors)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        category = self.request.query_params.get('category', None)
        if category is not None:
            category = Category.objects.get(category=category)
            serializer = CategorySerializer(category, data=data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(status=200)
            else:
                raise Exception(serializer.errors)
        else:
            raise Exception('Category is required')

    def delete(self, request, *args, **kwargs):
        category = self.request.query_params.get('category', None)
        if category is not None:
            category = Category.objects.get(category=category)
            category.delete()
            return HttpResponse(status=200)
        else:
            raise Exception('Category is required')


@csrf_exempt
def login(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        user = User.objects.get(username=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Username"
        return HttpResponse(json.dumps(dic))
    if user.password != password:
        dic['message'] = "Wrong Password"
        dic['status'] = "Failed"
        return HttpResponse(json.dumps(dic))
    else:
        dic['status'] = "Success"
        dic['user_id'] = user.id
        dic['user_role'] = user.role
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def register(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        role = post_content['role']
        user = User.objects.get(username=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Success"
        newUser = User(username=username, password=password, role=role)
        newUser.save()
        return HttpResponse(json.dumps(dic))
    if user is not None:
        dic['status'] = "Failed"
        dic['message'] = "User exist"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def randomMovie(request):
    max_id = Movie.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(62830, max_id)
        movie = Movie.objects.filter(pk=pk).first()
        if movie is not None:
            movie_serializer = MovieSerializer(movie)
            return HttpResponse(json.dumps(movie_serializer.data))


@csrf_exempt
def randomPerson(request):
    max_id = Person.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(3465784, max_id)
        person = Person.objects.filter(pk=pk).first()
        if person is not None:
            person_serializer = PersonSerializer(person)
            return HttpResponse(json.dumps(person_serializer.data))