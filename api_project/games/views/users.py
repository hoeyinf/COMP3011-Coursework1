"""Defines the views for API endpoints regarding users."""
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Review, User
from ..serializers import ReviewSerializer, UserSerializer


class Users(APIView):
    """Views for creating and viewing users (POST, GET)"""

    def post(self, request, *args, **kwargs):
        """View for POST /users/"""
        # Checks that the correct endpoint (without user id) is being used
        if "pk" in kwargs:
            return Response({"message": "Wrong API endpoint. Use: "\
                                        "POST api/users/"},
                            status=status.HTTP_400_BAD_REQUEST)

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
        """View for GET /users/{user_id}"""
        if "pk" not in kwargs:
            return Response({"message": "User id not provided in url."},
                            status=status.HTTP_404_NOT_FOUND)
        else: pk = kwargs["pk"]
        try:
            user = User.objects.get(pk=pk)

            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": f"User with id={pk} not found."},
                            status=status.HTTP_404_NOT_FOUND)


class UserReviews(generics.ListAPIView):
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    
    def get(self, request, pk):
        """View for GET /users/{user_id}/reviews/"""
        try:
            user = User.objects.get(pk=pk)
            reviews = self.queryset.filter(user=user).order_by('-date')
            pages = self.paginate_queryset(reviews)
            serializer = ReviewSerializer(pages, context={'request': request},
                                          many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": f"User with id={pk} not found."},
                            status=status.HTTP_404_NOT_FOUND)