"""
Defines the views for the different API endpoints. Simply displays the json
responses.
"""
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *


class UserProfile(APIView):
    """View for user profile."""

    def get_object(self, pk):
        """Retrieves user using primary key."""
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """View for GET /api/users/<user_id>"""
        user = self.get_object(pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReviews(APIView):
    """View for seeing a user's reviews."""

    def get_object(self, pk):
        """Retrieves a user's reviews using user's id."""
        try:
            user = User.objects.get(pk=pk)
            return Review.objects.filter(user=user)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """View for GET /api/users/<user_id>/reviews"""
        reviews = self.get_object(pk)
        serializer = ReviewSerializer(reviews, context={'request': request},
                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Reviews(APIView):
    """Views for reviews."""
    
    def get_object(self, pk):
        """Retrieves review using primary key."""
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        """View for GET /api/reviews/<review_id>"""
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class Games(APIView):
    """View for games."""
    
    def get_object(self, pk):
        """Retrieves game using primary key."""
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        """View for GET /api/games/<game_id>"""
        review = self.get_object(pk)
        serializer = GameSerializer(review, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
