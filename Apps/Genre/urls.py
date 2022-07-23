from django.urls import path

from Apps.Genre.views import GenreAPIView, GenreDetailAPIView, GenreMovieAPIView, GenreMovieDetailAPIView

urlpatterns = [
    path('', GenreAPIView.as_view(), name='get_post_genres'),
    path('<int:genre_id>', GenreDetailAPIView.as_view(), name='genres_details'),
    path('assignment-to-movie', GenreMovieAPIView.as_view(), name='post_genremovie'),
    path('details/<int:genre_movie_id>', GenreMovieDetailAPIView.as_view(), name='genremovie_details')
]