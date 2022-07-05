import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from Apps.Genre.models import Genre, GenreMovie
from Apps.Genre.serializers import GenreSerializer
from Apps.Movie.models import Movie

# Create your tests here.

class GenreTests(APITestCase):
    """ Test module for Genre model """

    # FIXME: Add authentication in the tests

    # Test preparation
    def setUp(self):
        """Generate data for tests
        """
        Genre.objects.create(name='Acción')
        Genre.objects.create(name='Aventura')
        Genre.objects.create(name='Crimen')

    # GET all Genres
    def test_get_genres(self):
        """Criteria:
        - status code == 200 OK
        - records == 3
        - the same response
        """
        response = self.client.get(reverse('get_post_genres'))
        genres = Genre.objects.all()
        genre_serializer = GenreSerializer(genres, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data, genre_serializer.data)

    # POST a new Genre
    def test_post_genre(self):
        """Criteria:
        - status code == 201 CREATED
        - message in response == 'Genre created successfully'
        - Compare the name in the response with the query
        """
        response = self.client.post(
            reverse('get_post_genres'),
            data=json.dumps({ 'name': 'Fantasia' }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Genre created successfully")
        self.assertEqual(response.data['data']['name'], Genre.objects.get(pk=4).name)

    # UPDATE the Genre with ID: 3
    def test_put_genre(self):
        """Criteria:
        - status code == 200 OK
        - message in response == 'Genre with ID:3 was updated successfully'
        - Compare the name in the response with the query
        """
        response = self.client.put(
            reverse('genres_details', kwargs={'id': 3}),
            data=json.dumps({ 'name': 'Comedia' }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Genre with ID:3 was updated successfully")
        self.assertEqual(response.data['data']['name'], Genre.objects.get(pk=3).name)

    # DELETE the Genre with ID: 3
    def test_delete_genre(self):
        """Criteria:
        - status code == 200 OK
        - message in response == 'Genre with ID:3 was deleted successfully'
        - records == 2
        """
        response = self.client.delete(reverse('genres_details', kwargs={'id': 3}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Genre with ID:3 was deleted successfully")
        self.assertEqual(len(Genre.objects.all()), 2)

class GenreMovieTests(APITestCase):
    """ Test module for GenreMovie model """

    # Test preparation
    def setUp(self):
        """Generate data for tests
        """
        Genre.objects.create(name='Aventura')
        self.genre = Genre.objects.create(name='Acción')
        self.movie = Movie.objects.create(title='John Wick', year=2014, resume='John Wick')
        GenreMovie.objects.create(movie=self.movie, genre=self.genre)

    # POST a new GenreMovie record
    def test_post_genre_movie(self):
        """Criteria:
        - status code == 201 CREATED
        - message in response == 'Genre assigned at Movie successfully'
        """
        response = self.client.post(
            reverse('post_genremovie'),
            data=json.dumps({ 'movie': 1, 'genre': 2 }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Genre assigned at Movie successfully")

    # UPDATE the GenreMovie record with ID: 1
    def test_put_genre(self):
        """Criteria:
        - status code == 200 OK
        - message in response == 'The record with ID:1 was updated successfully'
        """
        response = self.client.put(
            reverse('genremovie_details', kwargs={'id': 1}),
            data=json.dumps({ 'genre': 2 }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "The record with ID:1 was updated successfully")

    # DELETE the Genre with ID: 1
    def test_delete_genre(self):
        """Criteria:
        - status code == 200 OK
        - message in response == 'The record with ID:1 was deleted successfully'
        - records == 2
        """
        response = self.client.delete(reverse('genremovie_details', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "The record with ID:1 was deleted successfully")
        self.assertEqual(len(Genre.objects.all()), 2)