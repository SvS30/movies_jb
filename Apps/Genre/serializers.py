from rest_framework import serializers

from Apps.Genre.models import Genre, GenreMovie
from Apps.Movie.models import Movie

class GenreSerializer(serializers.Serializer):
    # Fiels
    name = serializers.CharField(max_length=50)

    # Relationship
    movies = serializers.StringRelatedField(many=True, required=False)

    # Methods
    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    class Meta:
        model = Genre
        fields = ['name', 'movies']

class GenreMovieSerializer(serializers.Serializer):
    # Fields
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    # Methods
    def create(self, validated_data):
        return GenreMovie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.genre = validated_data.get('genre', instance.genre)
        instance.movie = validated_data.get('movie', instance.movie)
        instance.save()
        return instance

    class Meta:
        model = GenreMovie
        fields = ['genre', 'movie']