from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from json import dumps

# Create your tests here.

class AuthTokenTestCase(APITestCase):
    """ Test module for Authentication """

    # Test preparation
    def setUp(self):
        """Generate data

        Steps:
            1. Create a new user.
            2. Create a token by the new user.
        """
        user_by_tests = User.objects.create_user(username='root', password='123456')
        Token.objects.get_or_create(user=user_by_tests)

    def test_failed_login_by_user_not_found(self):
        """Test login failed by user not found

        Criteria:
            - status code == 400 BAD REQUEST
            - message == 'Authentication Failed'
            - error == 'User not found'
        """
        response = self.client.post(
            reverse('login'),
            data=dumps({
                'username':'alberto',
                'password':'123456'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Authentication Failed")
        self.assertEqual(response.data['error'], "User not found")

    def test_failed_login_by_passwd_incorrect(self):
        """Test login failed by password incorrect

        Criteria:
            -  status code == 400 BAD REQUEST
            - message == 'Authentication Failed'
            - error == 'Password incorrect'
        """
        response = self.client.post(
            reverse('login'),
            data=dumps({
                'username':'root',
                'password':'654321'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Authentication Failed")
        self.assertEqual(response.data['error'], "Password incorrect")

    def test_success_login(self):
        """Test success login
        
        Criteria
            - status code == 200 OK
            - message == 'Authentication successfully'
            - user == 'root'
        """
        response = self.client.post(
            reverse('login'),
            data=dumps({
                'username':"root",
                'password':"123456"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Authentication successfully")
        self.assertEqual(response.data['user'], "root")

    def test_logout(self):
        """Test success logout by Header 'Authorization: Token'

        Criteria:
            - status code == 200 OK
            - message == 'Logout successfully'
        """
        token = Token.objects.get(user__username='root')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Logout successfully")