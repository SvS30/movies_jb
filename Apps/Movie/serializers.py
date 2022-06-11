from rest_framework import serializers

from Apps.Movie.models import Movie, MovieImage

class MovieSerializer(serializers.Serializer):
    # Fields
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=50)
    year = serializers.IntegerField()
    resume = serializers.CharField()
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    count_reviews = serializers.IntegerField(default=0)

    # Relationships
    images = serializers.StringRelatedField(many=True, required=False)
    genres = serializers.StringRelatedField(many=True, required=False)
    reviews = serializers.StringRelatedField(many=True, required=False)

    # Methods
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.resume = validated_data.get('resume', instance.resume)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.count_reviews = validated_data.get('count_reviews', instance.count_reviews)
        instance.save()
        return instance

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'resume', 'rating', 'count_reviews', 'images', 'genres']

class MovieImageSerializer(serializers.Serializer):
    # Fields
    path = serializers.FileField()
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), many=False)
    is_feature = serializers.BooleanField()

    # Methods
    def create(self, validated_data):
        return MovieImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.path = validated_data.get('path', instance.path)
        instance.movie = validated_data.get('movie', instance.movie)
        instance.is_feature = validated_data.get('is_feature', instance.is_feature)
        instance.save()
        return instance

    class Meta:
        model = MovieImage
        fields = ['path', 'is_feature', 'movie']