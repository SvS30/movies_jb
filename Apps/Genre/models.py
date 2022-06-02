from django.db import models

from Apps.Movie.models import Movie

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genres'

class GenreMovie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='genres')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}: {1}".format(self.genre, self.movie)

    class Meta:
        db_table = 'genre_movies'