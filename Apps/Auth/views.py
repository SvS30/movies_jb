from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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