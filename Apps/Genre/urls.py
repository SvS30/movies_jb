from django.urls import re_path

from Apps.Genre.views import GenreAPIView, GenreDetailAPIView, GenreMovieAPIView, GenreMovieDetailAPIView

urlpatterns = [
    re_path('^$', GenreAPIView.as_view(), name='get_post_genres'),
    re_path('^(?P<id>\d+)$', GenreDetailAPIView.as_view(), name='genres_details'),
    re_path('^assignment-to-movie$', GenreMovieAPIView.as_view(), name='post_genremovie'),
    re_path('^details/(?P<id>\d+)$', GenreMovieDetailAPIView.as_view(), name='genremovie_details')
]