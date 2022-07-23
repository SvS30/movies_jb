from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from Apps.Genre.models import Genre, GenreMovie
from Apps.Genre.serializers import GenreMovieSerializer, GenreSerializer

# Create your views here.

class GenreAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to represents some Genre endpoints
    
    Methods availables : GET, POST
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def get(self, request, format=None):
        """Return a list of all genres

        Args:
            request (rest_framework.request): Request received
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        movies = Genre.objects.order_by('created_at')
        queryset = GenreSerializer(movies, many=True)
        return Response(queryset.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """Save a new genre

        Args:
            request (rest_framework.request): Request received
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        genre_data = JSONParser().parse(request)
        is_duplicated = Genre.objects.filter(name=genre_data['name']).exists()
        if not is_duplicated:
            genre_serialized = GenreSerializer(data=genre_data)
            if genre_serialized.is_valid():
                genre_serialized.save()
                return Response({
                    'message': 'Genre created successfully',
                    'data': genre_serialized.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'message': 'Error in saved to new Genre',
                'errors': genre_serialized.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'message': 'Error in saved to new Genre',
                'errors': { 'name': 'This genre has already been registered' }
            }, status=status.HTTP_400_BAD_REQUEST)

class GenreDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to represents some Genre endpoints
    
    Methods availables : GET, PUT, DELETE
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def get_object(self, id):
        """Search if exists the genre with that id

        Args:
            id: Genre'id
        """
        try:
            return Genre.objects.get(pk=id)
        except Genre.DoesNotExist:
            return 404

    def get(self, request, genre_id, format=None):
        """Return a Genre

        Args:
            request (rest_framework.request): Request received
            genre_id (int): Genre'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        genre = self.get_object(genre_id)
        if genre != 404:
            queryset = GenreSerializer(genre, many=False)
            return Response(queryset.data, status=status.HTTP_200_OK)
        return Response({
            'message': 'Genre not found',
        }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, genre_id, format=None):
        """Update a genre

        Args:
            request (rest_framework.request): Request received
            genre_id (int): Genre'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        genre = self.get_object(genre_id)
        if genre != 404:
            genre_data = JSONParser().parse(request)
            genre_serialized = GenreSerializer(genre, data=genre_data, partial=True)
            if genre_serialized.is_valid():
                genre_serialized.save()
                return Response({
                    'message': f'Genre with ID:{genre_id} was updated successfully',
                    'data': genre_serialized.data
                }, status=status.HTTP_200_OK)
            return Response({
                'message': f'Error in update the genre with ID: {genre_id}',
                'errors': genre_serialized.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'message': 'Genre not found',
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, genre_id, format=None):
        """Delete a genre

        Args:
            request (rest_framework.request): Request received
            genre_id (int): Genre'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        genre = self.get_object(genre_id)
        if genre != 404:
            genre.delete()
            return Response({
                'message': f'Genre with ID:{genre_id} was deleted successfully'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Genre not found',
        }, status=status.HTTP_404_NOT_FOUND)

class GenreMovieAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to assign movies to genres
    
    Methods availables : POST
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def post(self, request, format=None):
        """Save a new assign movie to genre

        Args:
            request (rest_framework.request): Request received
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        assignment_data = JSONParser().parse(request)
        assignment_serialized = GenreMovieSerializer(data=assignment_data)
        if assignment_serialized.is_valid():
            assignment_serialized.save()
            return Response({
                'message': 'Genre assigned at Movie successfully',
                'data': assignment_serialized.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Error assigning the genre to the movie',
            'errors': assignment_serialized.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class GenreMovieDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Class used to represents some GenreMovie endpoints
    
    Methods availables : PUT, DELETE
    Authentication:
        Token required in Header:
            Authorization: Token {token}
    """
    def get_object(self, id):
        """Search if exists the record with that id

        Args:
            id: GenreMovie'id
        """
        try:
            return GenreMovie.objects.get(pk=id)
        except GenreMovie.DoesNotExist:
            return 404

    def put(self, request, genre_movie_id, format=None):
        """Update a record

        Args:
            request (rest_framework.request): Request received
            genre_movie_id (int): GenreMovie'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        record = self.get_object(genre_movie_id)
        if record != 404:
            assignment_data = JSONParser().parse(request)
            assignment_serialized = GenreMovieSerializer(record, data=assignment_data, partial=True)
            if assignment_serialized.is_valid():
                assignment_serialized.save()
                return Response({
                    'message': f'The record with ID:{genre_movie_id} was updated successfully',
                    'data': assignment_serialized.data
                }, status=status.HTTP_200_OK)
            return Response({
                'message': f'Error in update the record with ID: {genre_movie_id}',
                'errors': assignment_serialized.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'message': f'The record with ID:{genre_movie_id} not found',
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, genre_movie_id, format=None):
        """Delete a record

        Args:
            request (rest_framework.request): Request received
            genre_movie_id (int): GenreMovie'id
            format: Defaults to None.

        Returns:
            rest_framework.Response
        """
        record = self.get_object(genre_movie_id)
        if record != 404:
            record.delete()
            return Response({
                'message': f'The record with ID:{genre_movie_id} was deleted successfully'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': f'The record with ID:{genre_movie_id} not found',
        }, status=status.HTTP_404_NOT_FOUND)