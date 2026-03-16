"""
Defines the views for the different API endpoints. Simply displays the json
responses.
"""
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models import Count
from django.http import Http404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


@api_view(['POST'])
def post_users(request):
    """View for creating new user."""
    if request.method == "GET":
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "POST":
        if 'username' not in request.data or 'password' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        password = request.data['password']
        
        # Checks username length
        if len(username) < 3:
            return Response({"message": f"Username '{username}' is too short."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Checks username uniqueness
        try:
            user = User.objects.get(username=username)
            return Response({"message": f"Username '{username} already taken'"},
                            status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            pass
        
        # Validates password using default validators defined in settings.py
        try:
            validate_password(password=password)
        except ValidationError:
            return Response({"message": "Invalid password. Must be at least"\
                                        "12 characters long with letters."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Creates user
        user = User.objects.create_user(username=username, password=password)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class GamesList(generics.ListAPIView):
    queryset = Game.objects.all().order_by('-release_date')
    pagination_class = PageNumberPagination
    
    def validate_params(self, params):
        """Validates provided query paramaters and raises 404 if unknown."""
        known = ['genre', 'platform', 'developer', 'publisher', 'page']
        for param in params:
            if param not in known:
                raise Http404
    
    def get_queryset(self):
        """Filters queryset based on query parameters."""
        self.validate_params(self.request.query_params)
        genre = self.request.query_params.get('genre')
        platform = self.request.query_params.get('platform')
        developer = self.request.query_params.get('developer')
        publisher = self.request.query_params.get('publisher')
        if genre is not None:
            self.queryset = self.queryset.filter(genre__name__iexact=genre)
        if platform is not None:
            self.queryset = self.queryset.filter(platforms__name__iexact=platform)
        if developer is not None:
            self.queryset = self.queryset.filter(developers__name__iexact=developer)
        if publisher is not None:
            self.queryset = self.queryset.filter(publishers__name__iexact=publisher)
        return super().get_queryset()
    
    def get(self, request):
        """View for GET /api/games/"""
        games = self.get_queryset()
        pages = self.paginate_queryset(games)
        serializer = GameSerializer(pages, context={'request': request},
                                    many=True, fields=['id', 'title', 'url',
                                                       'release_date'])
        return Response(serializer.data, status=status.HTTP_200_OK)
        


@api_view()
def get_games_id(request, pk):
    """View for GET /api/games/<game__id>"""
    try:
        game = Game.objects.annotate(reviews_n=Count("review")).get(pk=pk)
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class UserReviews(generics.ListAPIView):
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    
    def get(self, request, pk):
        """View for GET /api/users/<user__id>/reviews/"""
        try:
            user = User.objects.get(pk=pk)
            reviews = self.queryset.filter(user=user).order_by('-date')
            pages = self.paginate_queryset(reviews)
            serializer = ReviewSerializer(pages, context={'request': request},
                                          many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GameReviews(generics.ListAPIView):
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    
    def get(self, request, pk):
        """View for GET /api/games/<game__id>/reviews/"""
        try:
            game = Game.objects.get(pk=pk)
            reviews = self.queryset.filter(game=game).order_by('-date')
            pages = self.paginate_queryset(reviews)
            serializer = ReviewSerializer(pages, context={'request': request},
                                          many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
