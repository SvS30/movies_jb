from django.urls import path

from Apps.UserActions.views import FavoriteAPIView, ReviewAPIView

urlpatterns = [
    path('post-review', ReviewAPIView.as_view(), name='post_review'),
    path('movie-favorite', FavoriteAPIView.as_view(), name='favorite_movie'),
    path('get-favorites', FavoriteAPIView.as_view())
]