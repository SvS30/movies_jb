from django.urls import re_path

from Apps.UserActions.views import FavoriteAPIView, ReviewAPIView

urlpatterns = [
    re_path('^post-review$', ReviewAPIView.as_view(), name='post_review'),
    re_path('^movie-favorite$', FavoriteAPIView.as_view(), name='favorite_movie'),
    re_path('^get-favorites$', FavoriteAPIView.as_view())
]