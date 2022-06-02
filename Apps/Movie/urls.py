from django.urls import re_path

from Apps.Movie.views import MovieImageAPIView, MovieImageDetailAPIView, MoviesAPIView, MovieDetailAPIView

urlpatterns = [
    re_path('^$', MoviesAPIView.as_view(), name='get_post_movies'),
    re_path('^(?P<id>\d+)$', MovieDetailAPIView.as_view(), name='movies_details'),
    re_path('^upload-image$', MovieImageAPIView.as_view()),
    re_path('^image/(?P<id>\d+)$', MovieImageDetailAPIView.as_view())
]