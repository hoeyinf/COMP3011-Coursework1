"""
Defines the views for the different API endpoints. Simply displays the json
responses.
"""
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg, Count
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

class Users(APIView):
    """Views for creating and viewing users (POST, GET)"""

    def post(self, request):
        """View for POST /api/users/"""
        if request.method == "GET":
            return Response(
                {"message": "User id not provided in url.\n"\
                            "Format: GET /api/users/<user_id>"},
                status=status.HTTP_404_NOT_FOUND
                )
        
        elif request.method == "POST":
            # Checks that provided request data is appropriate
            fields = ["username", "password"]
            if any(field not in fields for field in request.data):
                return Response(
                    {"message":f"Provided data fields are incorrect."},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            if not all(field in request.data for field in fields):
                return Response({"message": f"Username/password not provided."},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            username = request.data['username']
            password = request.data['password']
            
            # Checks username length
            if len(username) < 3:
                return Response(
                    {"message": f"Username '{username}' is too short."},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validates password using default validators defined in settings.py
            try:
                validate_password(password=password)
            except ValidationError:
                return Response(
                    {"message": "Invalid password. Must be at least 12 "\
                                "characters long with letters."},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Checks username uniqueness
            try:
                user = User.objects.get(username=username)
                return Response(
                    {"message": f"Username '{username}' already taken."},
                    status=status.HTTP_409_CONFLICT
                    )
            except User.DoesNotExist:
                pass

            # Creates user
            user = User.objects.create_user(username=username, password=password)
            serializer = UserSerializer(user, context={'request': request},
                                        fields=["username", "url"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """View for GET /api/users/<user__id>"""
        if "pk" not in self.kwargs:
            return Response({"message": "User id not provided in url."},
                            status=status.HTTP_404_NOT_FOUND)
        else: pk = self.kwargs["pk"]
        try:
            user = User.objects.annotate(
                reviews_n=Count("review"),
                average_review_score=Avg("review__score")).get(pk=pk)

            # Gathers histogram data
            reviews = Review.objects.filter(user__id=user.id)
            reviews_hist = [reviews.filter(score__lte=20).count(),
                            reviews.filter(score__gt=20, score__lte=40).count(),
                            reviews.filter(score__gt=40, score__lte=60).count(),
                            reviews.filter(score__gt=60, score__lte=80).count(),
                            reviews.filter(score__gt=80, score__lte=100).count()]
            
            serializer = UserSerializer(user,
                                        context={'request': request,
                                                 'reviews_hist': reviews_hist})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Reviews(APIView):
    """Views for CRUD on reviews (POST, GET, PATCH, DELETE)"""
            
    def get(self, request, *args, **kwargs):
        """View for GET /api/reviews/<review__id>"""

        # Check that id is provided
        if "pk" not in self.kwargs:
            return Response({"message": "Review id not provided in url."},
                            status=status.HTTP_404_NOT_FOUND)
        else: pk = self.kwargs["pk"]
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({"message": f"Review with id={pk} not found."},
                            status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        """View for POST /api/reviews/"""
        fields = ["game", "date", "score", "content"]
        
        if request.user.is_authenticated:
            # Checks that fields provided are correct
            if any(key not in fields for key in request.data):
                return Response({"message": "Provided fields are incorrect."},
                                status=status.HTTP_400_BAD_REQUEST)
            elif not all(key in request.data for key in fields):
                return Response({"message": "Required fields not provided."},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                # Checks that review does not already exist
                game = Game.objects.get(pk=request.data["game"])
                review = Review.objects.filter(user__id=request.user.id,
                                               game__id=game.id)
                if len(review) != 0:
                    return Response({"message": "Review already exists."},
                                    status=status.HTTP_409_CONFLICT)

            # Responds with error if game is invalid
            except Game.DoesNotExist:
                return Response(
                    {"message": "Game with id="\
                                 f"{request.data["game"]} not found."},
                    status=status.HTTP_404_NOT_FOUND)
            
            # Deserializes data and creates new object in database
            serializer = ReviewSerializer(data=request.data,
                                          context={'request': request} )
            if serializer.is_valid():
                serializer.save(user=request.user, game=game)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Not authenticated (jwt not found)."},
                            status=status.HTTP_401_UNAUTHORIZED)
    
    def patch(self, request, *args, **kwargs):
        """View for PATCH /api/reviews/<review__id>"""

        if request.user.is_authenticated:
            # Checks that data provided is correct
            if "pk" not in kwargs:
                return Response({"message": "Review not provided."},
                                status=status.HTTP_400_BAD_REQUEST)
            pk = kwargs["pk"]
            if any(key not in ["score", "content"] for key in request.data):
                return Response({"message": "Provided fields are incorrect."},
                                status=status.HTTP_400_BAD_REQUEST)
            elif not("score" in request.data or "content" in request.data):
                return Response(
                    {"message": "Need to provide score or content to update."},
                    status=status.HTTP_400_BAD_REQUEST)
            
            # Checks that review exists and that user is the author
            try:
                review = Review.objects.get(pk=pk)
                if review.user != request.user:
                    return Response({"message": "You are not the author."},
                                    status=status.HTTP_403_FORBIDDEN)
            except Review.DoesNotExist:
                return Response({"message": f"Review with id={pk} not found."},
                                status=status.HTTP_404_NOT_FOUND)

            # Deserializes data and saves updated object in database
            serializer = ReviewSerializer(review, data=request.data,
                                          context={'request': request},
                                          partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data=serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Not authenticated (jwt not found)."},
                            status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, *args, **kwargs):
        """View for DELETE /api/reviews/<review__id>"""
        if request.user.is_authenticated:
            if "pk" not in kwargs:
                return Response({"message": "Review not provided."},
                                status=status.HTTP_400_BAD_REQUEST)
            pk = kwargs["pk"]
            try:
                review = Review.objects.get(pk=pk)
                if review.user.id != request.user.id:
                    return Response({"message": "You are not the author."},
                                    status=status.HTTP_403_FORBIDDEN)
                review.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Review.DoesNotExist:
                return Response({"message": "Review not found."},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Not authenticated (jwt not found)."},
                            status=status.HTTP_401_UNAUTHORIZED)


class Games(generics.ListAPIView):
    queryset = Game.objects.all().order_by('-release_date')
    pagination_class = PageNumberPagination
    known_params = ["genre", "platform", "developer", "publisher", "page", "name"]
    
    def get_queryset(self, request):
        """Filters queryset based on query parameters."""
        genre = request.query_params.get("genre")
        platform = request.query_params.get("platform")
        developer = request.query_params.get("developer")
        publisher = request.query_params.get("publisher")
        name = request.query_params.get("name")
        if genre is not None:
            self.queryset = self.queryset.filter(genre__name__iexact=genre)
        if platform is not None:
            self.queryset = self.queryset.filter(platforms__name__iexact=platform)
        if developer is not None:
            self.queryset = self.queryset.filter(developers__name__iexact=developer)
        if publisher is not None:
            self.queryset = self.queryset.filter(publishers__name__iexact=publisher)
        if name is not None:
            self.queryset = self.queryset.filter(title__icontains=name)

        return super().get_queryset()
    
    def get(self, request, *args, **kwargs):
        """View for GET /api/games/ and GET /api/games/<game__id>"""
        if "pk" in kwargs:
            pk = kwargs["pk"]
            try:
                game = Game.objects.annotate(reviews_n=Count("review")).get(pk=pk)
                serializer = GameSerializer(game, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Game.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
        # Checks that parameters are correct
            if any(param not in self.known_params
                   for param in request.query_params):
                return Response(status=status.HTTP_404_NOT_FOUND)

            games = self.get_queryset(request)
            pages = self.paginate_queryset(games)
            serializer = GameSerializer(pages, context={'request': request},
                                        many=True, fields=['id', 'title', 'url',
                                                        'release_date'])
            return Response(serializer.data, status=status.HTTP_200_OK)


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
