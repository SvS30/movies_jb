from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
import json

from Apps.Movie.models import Movie

# Create your tests here.

class ReviewTestCase(APITestCase):
    """ Test module for Review model """

    # Test preparation
    def setUp(self):
        """Generate data for tests
        """
        self.user = User.objects.create_user(username='root', password='123456')
        self.token = Token.objects.get_or_create(user=self.user)
        self.api_authentication()
        self.movie = Movie.objects.create(title='John Wick', year=2014, resume='John Wick')
        self.user = User.objects.create(username='client1', password='client123', is_superuser='0')

    def api_authentication(self):
        """Function to add the Authorization Header
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token[0]}")

    def test_post_review(self):
        """Criteria:
        - status code == 201 CREATED
        - message in response == 'Review saved successfully at Movie with ID:1'
        """
        response = self.client.post(
            reverse('post_review'),
            data=json.dumps({
                'user': self.user.id,
                'movie': 1,
                'rating': 4,
                'text': 'Good!'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Review saved successfully at Movie with ID:1")

class FavoriteTestCase(APITestCase):
    """ Test module for Favorite model """

    # Test preparation
    def setUp(self):
        """Generate data for tests
        """
        self.user = User.objects.create_user(username='root', password='123456')
        self.token = Token.objects.get_or_create(user=self.user)
        self.api_authentication()
        self.movie = Movie.objects.create(title='John Wick', year=2014, resume='John Wick')

    def api_authentication(self):
        """Function to add the Authorization Header
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token[0]}")

    def test_post_review(self):
        """Criteria:
        - status code == 201 CREATED
        - message in response == 'Movie with ID:1 was add to User Favorite's with ID:{self.user.id}'
        """
        response = self.client.post(
            reverse('favorite_movie'),
            data=json.dumps({
                'user': self.user.id,
                'movie': self.movie.id,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], f"Movie with ID:1 was add to User Favorite's with ID:{self.user.id}")