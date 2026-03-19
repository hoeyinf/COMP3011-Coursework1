"""URLs for the games application."""
from django.urls import path
from games.views_api import *

urlpatterns = [
    path('users/', post_users, name='user-create'),
    path('users/<int:pk>', get_users_id, name="user-detail"),
    path('games/<int:pk>', get_games_id, name="game-detail"),
    path('reviews/<int:pk>', Reviews.as_view(), name="review-detail"),
    path('reviews/', Reviews.as_view(), name="review-detail"),
    path('games/', GamesList.as_view(), name="games"),
    path('users/<int:pk>/reviews/', UserReviews.as_view(), name="user-reviews"),
    path('games/<int:pk>/reviews/', GameReviews.as_view(), name="game-reviews")
]
