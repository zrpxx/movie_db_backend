from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
]

router = DefaultRouter(trailing_slash=False)
router.register(r'movies', views.MovieViewSet, basename='Movies')
router.register(r'comments', views.CommentViewSet, basename='Comments')
router.register(r'persons', views.PersonViewSet, basename='Persons')
router.register(r'categories', views.CategoryViewSet, basename='Categories')

urlpatterns += router.urls
