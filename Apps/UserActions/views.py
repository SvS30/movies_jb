from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Avg, Count

from Apps.Movie.models import Movie
from Apps.Movie.serializers import MovieSerializer
from Apps.UserActions.models import Favorite, Review
from Apps.UserActions.serializer import FavoriteSerializer, ReviewSerializer


# Create your views here.

class ReviewAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to represents some UserAction's endpoints
    
    Methods availables : POST
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def post(self, request, format=None):
        """Save a new Review's instance

        Args:
            request (rest_framework.request): Request received
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        review_data = {
            'user': request.user.id,
            'movie': request.data['movie'],
            'rating': request.data['rating'],
            'text': request.data['text']
        }
        review_serialized = ReviewSerializer(data=review_data)
        if review_serialized.is_valid():
            review_serialized.save()
            movie_update_rating = Movie.objects.get(pk=review_serialized.validated_data.get('movie').id)
            avg_rating = Review.objects.filter(movie=movie_update_rating.id).aggregate(Avg('rating'))
            count_reviews = Review.objects.filter(movie=movie_update_rating.id).aggregate(Count('text'))
            movie_data = {
                'rating': round(avg_rating['rating__avg'], 2),
                'count_reviews': count_reviews['text__count']
            }
            movie_to_update_serialized = MovieSerializer(movie_update_rating, data=movie_data, partial=True)
            if movie_to_update_serialized.is_valid():
                movie_to_update_serialized.save()
                return Response({
                    'message': f"Review saved successfully at Movie with ID:{review_serialized.data['movie']}",
                    'data': review_serialized.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': "Error in updated the Movie's rating",
                    'errors': movie_to_update_serialized.errors
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'message': 'Error in saved the new review',
            'errors': review_serialized.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class FavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to represents some MovieImage endpoints
    
    Methods availables : GET, POST
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def get(self, request, format=None):
        """Return a list of User Favorites Movie

        Args:
            request (rest_framework.request): Request received
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movies_favorites = Favorite.objects.filter(user=request.user.id)
        favorites_serialized = FavoriteSerializer(movies_favorites, many=True)
        return Response(favorites_serialized.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """Save a new Movie Favorite

        Args:
            request (rest_framework.request): Request received
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        favorite_data = {
            'user': request.user.id,
            'movie': request.data['movie']
        }
        favorite_serialized = FavoriteSerializer(data=favorite_data)
        if favorite_serialized.is_valid():
            favorite_serialized.save()
            return Response({
                'message': f"Movie with ID:{favorite_serialized.data['movie']} was add to User Favorite's with ID:{favorite_serialized.data['user']}",
                'data': favorite_serialized.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': "Error in added the Movie to User Favorite's",
            'errors': favorite_serialized.errors
        }, status=status.HTTP_400_BAD_REQUEST)
