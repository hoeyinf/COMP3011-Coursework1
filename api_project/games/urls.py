"""URLs for the games application."""
from django.urls import path
from games.views_api import *

urlpatterns = [
    path('users/', Users.as_view(), name='user-create'),
    path('users/<int:pk>', Users.as_view(), name="user-detail"),
    path('games/', Games.as_view(), name="games"),
    path('games/<int:pk>', Games.as_view(), name="game-detail"),
    path('reviews/<int:pk>', Reviews.as_view(), name="review-detail"),
    path('reviews/', Reviews.as_view(), name="review-detail"),
    path('users/<int:pk>/reviews/', UserReviews.as_view(), name="user-reviews"),
    path('games/<int:pk>/reviews/', GameReviews.as_view(), name="game-reviews")
]
