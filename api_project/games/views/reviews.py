"""Defines the views for API endpoints regarding reviews."""
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Game, Review
from ..serializers import ReviewSerializer


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
    
    def post(self, request, *args, **kwargs):
        """View for POST /api/reviews/"""
        fields = ["game", "date", "score", "content"]

        # Checks that the correct endpoint (without review id) is being used
        if "pk" in kwargs:
            return Response({"message": "Wrong API endpoint. Use: "\
                                        "POST api/reviews/"},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"message": "Not authenticated (jwt not found).",
                             "get_jwt": f"{request.get_host()}/api/token/"},
                             status=status.HTTP_401_UNAUTHORIZED)
    
    def patch(self, request, *args, **kwargs):
        """View for PATCH /api/reviews/<review__id>"""
        # Checks that data provided is correct
        if "pk" not in kwargs:
            return Response({"message": "Review not provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
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
        # Checks that review id was provided
        if "pk" not in kwargs:
            return Response({"message": "Review not provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            pk = kwargs["pk"]
            try:
                review = Review.objects.get(pk=pk)
                if review.user.id != request.user.id:
                    return Response({"message": "You are not the author."},
                                    status=status.HTTP_403_FORBIDDEN)
                review.delete()
                return Response({"message": f"Review deleted successfully."},
                                status=status.HTTP_204_NO_CONTENT)
            except Review.DoesNotExist:
                return Response({"message": "Review not found."},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Not authenticated (jwt not found).",
                             "get_jwt": f"{request.get_host()}/api/token/"},
                            status=status.HTTP_401_UNAUTHORIZED)
