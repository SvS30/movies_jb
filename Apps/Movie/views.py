from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from Apps.Movie.models import Movie, MovieImage
from Apps.Movie.serializers import MovieImageSerializer, MovieSerializer

# Create your views here.

class MoviesAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to represents some Movies endpoints
    
    Methods availables : GET, POST
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def get(self, request, format=None):
        """Return a list of all movies

        Args:
            request (rest_framework.request): Request received
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movies = Movie.objects.order_by('created_at')
        queryset = MovieSerializer(movies, many=True)
        return Response(queryset.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """Save a new movie

        Args:
            request (rest_framework.request): Request received
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movie_data = JSONParser().parse(request)
        movie_serialized = MovieSerializer(data=movie_data)
        if movie_serialized.is_valid():
            movie_serialized.save()
            return Response({
                'message': 'Movie created successfully',
                'data': movie_serialized.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Error in saved to new movie',
            'errors': movie_serialized.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class MovieDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to represents some Movies endpoints
    
    Methods availables : GET, PUT, DELETE
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def get_object(self, id):
        """Search if exists the movie with that id

        Args:
            id: Movie'id
        """
        try:
            return Movie.objects.get(pk=id)
        except Movie.DoesNotExist:
            return 404

    def get(self, request, movie_id, format=None):
        """Return a movie

        Args:
            request (rest_framework.request): Request received
            movie_id (int): Movie'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movie = self.get_object(movie_id)
        if movie != 404:
            queryset = MovieSerializer(movie, many=False)
            return Response(queryset.data, status=status.HTTP_200_OK)
        return Response({
            'message': 'Movie not found',
        }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, movie_id, format=None):
        """Update a movie

        Args:
            request (rest_framework.request): Request received
            movie_id (int): Movie'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movie = self.get_object(movie_id)
        if movie != 404:
            movie_data = JSONParser().parse(request)
            movie_serialized = MovieSerializer(movie, data=movie_data, partial=True)
            if movie_serialized.is_valid():
                movie_serialized.save()
                return Response({
                    'message': f'Movie with ID:{movie_id} was updated successfully',
                    'data': movie_serialized.data
                }, status=status.HTTP_200_OK)
            return Response({
                'message': f'Error in update the movie with ID: {movie_id}',
                'errors': movie_serialized.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'message': 'Movie not found',
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, movie_id, format=None):
        """Delete a movie

        Args:
            request (rest_framework.request): Request received
            movie_id (int): Movie'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movie = self.get_object(movie_id)
        if movie != 404:
            movie.delete()
            return Response({
                'message': f'Movie with ID:{movie_id} was deleted successfully'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Movie not found',
        }, status=status.HTTP_404_NOT_FOUND)

class MovieImageAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to represents some MovieImage endpoints
    
    Methods availables : POST
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def post(self, request, format=None):
        """Save a new Movie's image

        Args:
            request (rest_framework.request): Request received
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movie_image_serialized = MovieImageSerializer(data=request.data)
        if movie_image_serialized.is_valid():
            movie_image_serialized.save()
            return Response({
                'message': f"Image saved successfully at Movie with ID:{request.data['movie']}",
                'data': movie_image_serialized.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Error in saved the new image',
            'errors': movie_image_serialized.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class MovieImageDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to represents some MovieImage endpoints
    
    Methods availables : DELETE
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def get_object(self, id):
        """Search if exists the Movie's image with that id

        Args:
            id: MovieImage'id
        """
        try:
            return MovieImage.objects.get(pk=id)
        except MovieImage.DoesNotExist:
            return 404

    def delete(self, request, movie_image_id, format=None):
        """Delete a Movie's image

        Args:
            request (rest_framework.request): Request received
            movie_image_id (int): MovieImage'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        image = self.get_object(movie_image_id)
        if image != 404:
            image.delete()
            return Response({
                'message': f"Movie's image with ID:{movie_image_id} was deleted successfully"
            }, status=status.HTTP_200_OK)
        return Response({
            'message': "Movie's image not found",
        }, status=status.HTTP_404_NOT_FOUND)