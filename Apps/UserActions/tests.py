import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from Apps.Movie.models import Movie

# Create your tests here.

class ReviewTests(APITestCase):
    """ Test module for Review model """

    # Test preparation
    def setUp(self):
        """Generate data for tests
        """
        self.movie = Movie.objects.create(title='John Wick', year=2014, resume='John Wick')
        self.user = User.objects.create(username='client1', password='client123', is_superuser='0')

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

class FavoriteTest(APITestCase):
    """ Test module for Favorite model """

    # Test preparation
    def setUp(self):
        """Generate data for tests
        """
        self.movie = Movie.objects.create(title='John Wick', year=2014, resume='John Wick')
        self.user = User.objects.create(username='client1', password='client123', is_superuser='0')

    def test_post_review(self):
        """Criteria:
        - status code == 201 CREATED
        - message in response == 'Movie with ID:1 was add to User Favorite's with ID:{self.user.id}'
        """
        response = self.client.post(
            reverse('favorite_movie'),
            data=json.dumps({
                'user': self.user.id,
                'movie': 1,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], f"Movie with ID:1 was add to User Favorite's with ID:{self.user.id}")