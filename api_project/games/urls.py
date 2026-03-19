"""URLs for the games application."""
from django.urls import path
from .views.games import Games, GameReviews, get_game_analytics
from .views.reviews import Reviews
from .views.users import Users, UserReviews

urlpatterns = [
    path('users/', Users.as_view(), name='user-create'),
    path('users/<int:pk>', Users.as_view(), name="user-detail"),
    path('games/', Games.as_view(), name="games"),
    path('games/<int:pk>', Games.as_view(), name="game-detail"),
    path('games/<int:pk>/analytics', get_game_analytics, name="game-analytics"),
    path('reviews/<int:pk>', Reviews.as_view(), name="review-detail"),
    path('reviews/', Reviews.as_view(), name="review-detail"),
    path('users/<int:pk>/reviews/', UserReviews.as_view(), name="user-reviews"),
    path('games/<int:pk>/reviews/', GameReviews.as_view(), name="game-reviews")
]
