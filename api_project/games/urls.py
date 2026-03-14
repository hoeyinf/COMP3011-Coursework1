"""URLs for the games application."""
from django.urls import path
from games.views_api import *
from oauth2_provider import urls as oauth2_urls

urlpatterns = [
    path('users/<int:pk>', get_users_id, name="user-detail"),
    path('games/<int:pk>', get_game_id, name="game-detail"),
    path('reviews/<int:pk>', get_reviews_id, name="review-detail"),
    path('users/<int:pk>/reviews/', get_user_reviews, name="user-reviews"),
    path('games/<int:pk>/reviews/', get_game_reviews, name="game-reviews"),
    path('games/genres/', get_genres, name="game-genres"),
    path('games/genres/<int:pk>', get_genres_id, name="genre-detail"),
    path('games/platforms/', get_platforms, name="game-platforms"),
    path('games/platforms/<int:pk>', get_platforms_id, name="platform-detail"),
    path('games/developers/', get_developers, name="game-developers"),
    path('games/developers/<int:pk>', get_developers_id, name="developer-detail"),
    path('games/publishers/', get_publishers, name="game-publishers"),
    path('games/publishers/<int:pk>', get_publishers_id, name="publisher-detail")
]
