from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
import json

# Create your tests here.

class AuthTokenTest(APITestCase):
    """ Test module for Authentication """

    # TODO: Test case comments

    # Test preparation
    def setUp(self):
        """Generate data
        """
        user_by_tests = User.objects.create_user(username='root', password='123456')
        Token.objects.get_or_create(user=user_by_tests)

    def test_failed_login_by_user_not_found(self):
        response = self.client.post(
            reverse('login'),
            data=json.dumps({
                'username':'alberto',
                'password':'123456'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Authentication Failed")
        self.assertEqual(response.data['error'], "User not found")

    def test_failed_login_by_passwd_incorrect(self):
        response = self.client.post(
            reverse('login'),
            data=json.dumps({
                'username':'root',
                'password':'654321'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Authentication Failed")
        self.assertEqual(response.data['error'], "Password incorrect")

    def test_success_login(self):
        response = self.client.post(
            reverse('login'),
            data=json.dumps({
                'username':"root",
                'password':"123456"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Authentication successfully")
        self.assertEqual(response.data['user'], "root")

    def test_logout(self):
        token = Token.objects.get(user__username='root')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Logout successfully")