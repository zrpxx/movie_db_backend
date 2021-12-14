from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
]

router = DefaultRouter()
router.register(r'movies', views.MovieViewSet, basename='movies')
router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'persons', views.PersonViewSet, basename='Persons')
router.register(r'categories', views.CategoryViewSet, basename='Genres')

urlpatterns += router.urls
