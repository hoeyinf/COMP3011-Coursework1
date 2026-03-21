"""Defines the views for API endpoints regarding games."""
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from ..models import Game, Review
from ..serializers import GameAnalyticsSerializer, GamesAnalyticsSerializer, GameSerializer, ReviewSerializer


class Games(generics.ListAPIView, PageNumberPagination):
    queryset = Game.objects.all().order_by('-release_date')
    known_params = ["genre", "platform", "developer", "publisher", "page", "title"]
    
    def get_queryset(self):
        """Filters queryset based on query parameters."""
        genre = self.request.query_params.get("genre")
        platform = self.request.query_params.get("platform")
        developer = self.request.query_params.get("developer")
        publisher = self.request.query_params.get("publisher")
        title = self.request.query_params.get("title")
        if genre is not None:
            self.queryset = self.queryset.filter(genre__name__iexact=genre)
        if platform is not None:
            self.queryset = self.queryset.filter(platforms__name__iexact=platform)
        if developer is not None:
            self.queryset = self.queryset.filter(developers__name__iexact=developer)
        if publisher is not None:
            self.queryset = self.queryset.filter(publishers__name__iexact=publisher)
        if title is not None:
            self.queryset = self.queryset.filter(title__icontains=title)

        return super().get_queryset()
    
    def get(self, request, *args, **kwargs):
        """View for GET /games/ and GET /games/{game_id}"""
        if "pk" in kwargs:
            pk = kwargs["pk"]
            try:
                game = Game.objects.annotate(reviews_n=Count("review")).get(pk=pk)
                serializer = GameSerializer(game, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Game.DoesNotExist:
                return Response({"message": f"Game with id={pk} not found."},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            # Checks that parameters are correct
            if any(param not in self.known_params
                   for param in request.query_params):
                return Response({"message": f"Parameter name(s) not valid."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Gets analytics
            games = self.get_queryset()
            serializer = GamesAnalyticsSerializer(games,
                                                  context={'request': request})
            pages = self.paginate_queryset(games)
            # Gets games (paginated)
            game_pages = GameSerializer(
                pages, many=True, context={'request': request, 'games': games},
                fields=['title', 'url', 'release_date']
                )
            # Combines the two serializers into a paginated response
            return Response(
                {"analytics": serializer.data, "games": game_pages.data},
                status=status.HTTP_200_OK)


@api_view()
def get_game_analytics(request, pk):
    """View for GET /games/{game_id}/analytics"""
    try:
        game = Game.objects.get(pk=pk)
        serializer = GameAnalyticsSerializer(game, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Game.DoesNotExist:
        return Response({"message": f"Game with id={pk} not found."},
                        status=status.HTTP_404_NOT_FOUND)


class GameReviews(generics.ListAPIView):
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    
    def get(self, request, pk):
        """View for GET /games/{game_id}/reviews/"""
        try:
            game = Game.objects.get(pk=pk)
            reviews = self.queryset.filter(game=game).order_by('-date')
            pages = self.paginate_queryset(reviews)
            serializer = ReviewSerializer(pages, context={'request': request},
                                          many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({"message": f"Game with id={pk} not found."},
                            status=status.HTTP_404_NOT_FOUND)
