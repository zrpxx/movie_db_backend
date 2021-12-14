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

urlpatterns += router.urls
