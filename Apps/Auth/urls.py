from django.urls import path
from Apps.Auth.views import login, logout, oauth_login, oauth_redirect

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('oauth2', oauth_login, name='oauth_login'),
    path('oauth2/redirect', oauth_redirect, name='oauth_redirect')
]