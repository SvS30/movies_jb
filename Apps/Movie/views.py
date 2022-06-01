from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from Apps.Movie.models import Movie, MovieImage
from Apps.Movie.serializers import MovieImageSerializer, MovieSerializer

# Create your views here.

class MoviesAPIView(APIView):
    """Class used to represents some Movies endpoints
    
    Methods availables : GET, POST
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
    """Class used to represents some Movies endpoints
    
    Methods availables : GET, PUT, DELETE
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

    def get(self, request, id, format=None):
        """Return a movie

        Args:
            request (rest_framework.request): Request received
            id (int): Movie'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movie = self.get_object(id)
        if movie != 404:
            queryset = MovieSerializer(movie, many=False)
            return Response(queryset.data, status=status.HTTP_200_OK)
        return Response({
            'message': 'Movie not found',
        }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        """Update a movie

        Args:
            request (rest_framework.request): Request received
            id (int): Movie'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movie = self.get_object(id)
        if movie != 404:
            movie_data = JSONParser().parse(request)
            movie_serialized = MovieSerializer(movie, data=movie_data, partial=True)
            if movie_serialized.is_valid():
                movie_serialized.save()
                return Response({
                    'message': f'Movie with ID:{id} was updated successfully',
                    'data': movie_serialized.data
                }, status=status.HTTP_200_OK)
            return Response({
                'message': f'Error in update the movie with ID: {id}',
                'errors': movie_serialized.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'message': 'Movie not found',
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, format=None):
        """Delete a movie

        Args:
            request (rest_framework.request): Request received
            id (int): Movie'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movie = self.get_object(id)
        if movie != 404:
            movie.delete()
            return Response({
                'message': f'Movie with ID:{id} was deleted successfully'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Movie not found',
        }, status=status.HTTP_404_NOT_FOUND)

class MovieImageAPIView(APIView):
    """Class used to represents some MovieImage endpoints
    
    Methods availables : POST
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
    """Class used to represents some MovieImage endpoints
    
    Methods availables : DELETE
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

    def delete(self, request, id, format=None):
        """Delete a Movie's image

        Args:
            request (rest_framework.request): Request received
            id (int): MovieImage'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        image = self.get_object(id)
        if image != 404:
            image.delete()
            return Response({
                'message': f"Movie's image with ID:{id} was deleted successfully"
            }, status=status.HTTP_200_OK)
        return Response({
            'message': "Movie's image not found",
        }, status=status.HTTP_404_NOT_FOUND)