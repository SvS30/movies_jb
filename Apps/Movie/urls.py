from django.urls import path

from Apps.Movie.views import MovieImageAPIView, MovieImageDetailAPIView, MoviesAPIView, MovieDetailAPIView

urlpatterns = [
    path('', MoviesAPIView.as_view(), name='get_post_movies'),
    path('<int:movie_id>', MovieDetailAPIView.as_view(), name='movies_details'),
    path('upload-image', MovieImageAPIView.as_view()),
    path('image/<int:movie_image_id>', MovieImageDetailAPIView.as_view())
]