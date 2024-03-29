from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import requests

from Apps.Auth.models import DiscordUser

# Create your views here.

def valid_credentials(username, password):
    """Function to validate the credentials provided

    Args:
        username (str):
        password (str):

    Returns:
        error (str): str with the errors in validation
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        error = "User not found"
        return error
    passwd_validation = check_password(password, user.password)
    if not passwd_validation:
        error = "Password incorrect"
        return error

@api_view(['POST'])
def login(request, format=None):
    """Login

        Args:
            request (rest_framework.HttpRequest): Request received
            format Defaults to None.

        Returns:
            rest_framework.Response
        """
    errors = valid_credentials(request.data['username'], request.data['password'])
    if errors is None:
        user = authenticate(username=request.data['username'], password=request.data['password'])
        token,_ = Token.objects.get_or_create(user=user)
        if token:
            return Response({
                'message': 'Authentication successfully',
                'Token': f"{token}",
                'user': f"{user}"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Authentication Failed',
                'error': 'Token get or created failed',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            'message': 'Authentication Failed',
            'error': errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated])
def logout(request, format=None):
    """Logout

    Args:
        request: (rest_framework.HttpRequest): Request received
        format: Defaults to None.
    Returns:
        rest_framework.Response
    """
    request.user.auth_token.delete()
    return Response({
        'message': 'Logout successfully',
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def oauth_login(request, format=None):
    """Request auth with Discord

    Args:
        request: (rest_framework.HttpRequest): Request received
        format: Defaults to None.

    Returns:
        django.shortcuts.redirect: Redirect to Discord
    """
    return redirect(settings.OAUTH_URL)

@api_view(['GET'])
def oauth_redirect(request, format=None):
    """Request access_token to Discord and return User Data with AuthToken

    Args:
        request (rest_framework.HttpRequest): Request received
        format: Defaults to None.

    Returns:
        rest_framework.Response
    """
    if not 'error' in request.query_params:
        oauth_user, token = exchange_code(request.GET['code'])
        if oauth_user['verified']:
            find_user = DiscordUser.objects.filter(id=oauth_user['id']).exists()
            if find_user:
                discord_user = DiscordUser.objects.get(id=oauth_user['id'])
                user = User.objects.get(id=discord_user.user_id)
            else:
                user = User.objects.create(username=oauth_user['username'], email=oauth_user['email'])
                DiscordUser.objects.create_discord_user(user=oauth_user, user_id=user)
            token,_ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Authentication complete',
                'user': {
                    'username': oauth_user['username'],
                    'email': oauth_user['email'],
                    'avatar': oauth_user['avatar']
                },
                'Token': f"{token}"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Authentication incomplete',
                'error': 'Email not verified'
            }, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({
            'message': 'Authentication Failed',
            'error': 'Authorization denied'
        }, status=status.HTTP_403_FORBIDDEN)

def exchange_code(code):
    """Config Discord Request

    Args:
        code (str): Discord Authorization Code

    Returns:
        user_info (json): User info from Discord
        credentials (str): Access Token from Discord
    """
    data = {
        'client_id': settings.OAUTH_CLIENT_ID,
        'client_secret': settings.OAUTH_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.OAUTH_CALLBACK,
        'scope': 'identify'
    }
    response = requests.post('https://discord.com/api/oauth2/token', data, headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    credentials = response.json()
    user_info = requests.get('https://discord.com/api/v6/users/@me', headers={
        'Authorization': f"Bearer {credentials['access_token']}"
    })
    return user_info.json(), credentials['access_token']