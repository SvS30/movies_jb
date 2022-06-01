from rest_framework import serializers
from django.contrib.auth.models import User

from Apps.Movie.models import Movie
from Apps.UserActions.models import Favorite, Review

class ReviewSerializer(serializers.Serializer):
    # Fields
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), many=False)
    rating = serializers.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    text = serializers.CharField()

    # Methods
    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.movie = validated_data.get('movie', instance.movie)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

    class Meta:
        model = Review
        fields = ['user', 'movie', 'rating', 'text']

class FavoriteSerializer(serializers.Serializer):
    # Fields
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), many=False)

    # Methods
    def create(self, validated_data):
        return Favorite.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.movie = validated_data.get('movie', instance.movie)
        instance.save()
        return instance

    class Meta:
        model = Review
        fields = ['user', 'movie']