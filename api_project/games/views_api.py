"""
Defines the views for the different API endpoints. Simply displays the json
responses.
"""
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *


@api_view()
def get_users_id(request, pk):
    """View for GET /api/users/<user__id>"""
    try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view()
def get_reviews_id(request, pk):
    """View for GET /api/reviews/<review__id>"""
    try:
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view()
def get_game_id(request, pk):
    """View for GET /api/games/<game__id>"""
    try:
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view()
def get_user_reviews(request, pk):
    """View for GET /api/users/<user__id>/reviews/"""
    try:
        user = User.objects.get(pk=pk)
        reviews = Review.objects.filter(user=user)
        serializer = ReviewSerializer(reviews, context={'request': request},
                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view()
def get_game_reviews(request, pk):
    """View for GET /api/games/<game__id>/reviews/"""
    try:
        game = Game.objects.get(pk=pk)
        reviews = Review.objects.filter(game=game).order_by('-date')[:10]
        serializer = ReviewSerializer(reviews, context={'request': request},
                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view()
def get_genres(request):
    """View for GET /api/games/genres/"""
    genres = Genre.objects.all().order_by('name')
    serializer = GenreSerializer(genres, context={'request': request},
                                 many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_genres_id(request, pk):
    """View for GET /api/games/genres/<genre__id>"""
    try:
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Genre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view()
def get_platforms(request):
    """View for GET /api/games/platforms/"""
    platforms = Platform.objects.all().order_by('name')
    serializer = PlatformSerializer(platforms, context={'request': request},
                                    many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_platforms_id(request, pk):
    """View for GET /api/games/platforms/<platform__id>"""
    try:
        platform = Platform.objects.get(pk=pk)
        serializer = PlatformSerializer(platform, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Platform.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view()
def get_developers(request):
    """View for GET /api/games/developers/"""
    developers = Developer.objects.all().order_by('name')
    serializer = DeveloperSerializer(developers, context={'request': request},
                                     many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_developers_id(request, pk):
    """View for GET /api/games/developers/<developer__id>"""
    try:
        developer = Developer.objects.get(pk=pk)
        serializer = DeveloperSerializer(developer, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Developer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view()
def get_publishers(request):
    """View for GET /api/games/publishers/"""
    publishers = Publisher.objects.all().order_by('name')
    serializer = PublisherSerializer(publishers, context={'request': request},
                                     many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_publishers_id(request, pk):
    """View for GET /api/games/publishers/<publisher__id>"""
    try:
        publisher = Publisher.objects.get(pk=pk)
        serializer = PublisherSerializer(publisher, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Publisher.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
