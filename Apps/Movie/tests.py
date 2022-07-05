import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from Apps.Movie.models import Movie
from Apps.Movie.serializers import MovieSerializer

# Create your tests here.

class MovieTests(APITestCase):
    """ Test module for Movie model """

    # FIXME: Add authentication in the tests

    # Test preparation
    def setUp(self):
        """Generate data for tests
        """
        Movie.objects.create(title='John Wick', year=2014, resume='John Wick')
        Movie.objects.create(title='Nadie (Nobody)', year=2022, resume='Nadie (Nobody)')
        Movie.objects.create(title='PIRATAS DEL CARIBE: LA MALDICIÓN DE LA PERLA NEGRA', year=2014, resume='PIRATAS DEL CARIBE: LA MALDICIÓN DE LA PERLA NEGRA')

    # GET all Movies
    def test_get_movies(self):
        """Criteria:
        - status code == 200 OK
        - records == 3
        - the same response
        """
        response = self.client.get(reverse('get_post_movies'))
        movies = Movie.objects.all()
        movies_serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data, movies_serializer.data)

    # POST a new Movie
    def test_post_movie(self):
        """Criteria:
        - status code == 201 CREATED
        - message in response == 'Movie created successfully'
        - Compare the title in the response with the query
        """
        response = self.client.post(
            reverse('get_post_movies'),
            data=json.dumps({
                'title': 'ANIMALES FANTÁSTICOS Y DÓNDE ENCONTRARLOS',
                'year': 2016,
                'resume': 'ANIMALES FANTÁSTICOS Y DÓNDE ENCONTRARLOS'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Movie created successfully")
        self.assertEqual(response.data['data']['title'], Movie.objects.get(pk=4).title)

    # UPDATE the Movie with ID: 3
    def test_put_movie(self):
        """Criteria:
        - status code == 200 OK
        - message in response == 'Movie with ID:3 was updated successfully'
        - Compare the title in the response with the query
        """
        response = self.client.put(
            reverse('movies_details', kwargs={'id': 3}),
            data=json.dumps({
                'title': 'Piratas Del Caribe: La Maldición Del Perla Negra'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Movie with ID:3 was updated successfully")
        self.assertEqual(response.data['data']['title'], Movie.objects.get(pk=3).title)

    # DELETE the Movie with ID: 3
    def test_delete_movie(self):
        """Criteria:
        - status code == 200 OK
        - message in response == 'Movie with ID:3 was deleted successfully'
        - records == 2
        """
        response = self.client.delete(reverse('movies_details', kwargs={'id': 3}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Movie with ID:3 was deleted successfully")
        self.assertEqual(len(Movie.objects.all()), 2)