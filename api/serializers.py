from rest_framework import serializers

from api.models import Movie, Comment, Person, Category, MovieCategory, ActorMovie, DirectorMovie


class MovieCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCategory
        fields = '__all__'


class ActorMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorMovie
        fields = '__all__'


class DirectorMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorMovie
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
