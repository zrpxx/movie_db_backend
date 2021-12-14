import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import Movie, Comment, User, Category, Person
from .serializers import MovieSerializer, CommentSerializer, PersonSerializer, CategorySerializer


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def get_queryset(self):
        queryset = Movie.objects.all()
        movie_id = self.request.query_params.get('id', None)
        if movie_id is not None:
            queryset = queryset.filter(id=movie_id)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is not None:
            movie = MovieViewSet.queryset.filter(id=movie_id).first()
            if movie is not None:
                queryset = Comment.objects.filter(movie_id=movie)
            else:
                raise Exception('Movie not found')
        else:
            queryset = Comment.objects.all()
        return queryset



class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def get_queryset(self):
        queryset = Person.objects.all()
        person_id = self.request.query_params.get('id', None)
        if person_id is not None:
            queryset = queryset.filter(id=person_id)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = Category.objects.filter(category=category)
        else:
            queryset = Category.objects.all()
        return queryset


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
