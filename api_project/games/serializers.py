"""
Contains serializers that allow for easier serialization and deserialization of data into JSON
for API calls.
"""
import datetime
from django.db.models import Avg, Count
from rest_framework import serializers as s
from games.models import Game, Review, User


class DynamicFieldsSerializer(s.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer that uses a fields argument to control which
    fields to display.
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        # Keeps only fields that were specified
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class GameSerializer(DynamicFieldsSerializer):
    """Serializer for a game."""
    genre = s.CharField()
    platforms = s.SlugRelatedField(many=True, read_only=True, slug_field='name')
    developers = s.SlugRelatedField(many=True, read_only=True, slug_field='name')
    publishers = s.SlugRelatedField(many=True, read_only=True, slug_field='name')
    reviews = s.HyperlinkedIdentityField(view_name='game-reviews')
    analytics = s.HyperlinkedIdentityField(view_name='game-analytics')

    class Meta:
        model = Game
        fields = ["id", "title", "url", "release_date", "rating", "description",
                  "genre", "platforms", "developers", "publishers", "reviews",
                  "analytics"]


class UserSerializer(DynamicFieldsSerializer):
    """Serializer for a user."""

    reviews = s.HyperlinkedIdentityField(view_name='user-reviews')
    reviews_n = s.SerializerMethodField(method_name="get_reviews_n")
    average_score = s.SerializerMethodField(method_name="get_average_score")
    reviews_hist = s.SerializerMethodField(method_name="get_reviews_hist")
    favorite_genres = s.SerializerMethodField(method_name="get_favorite_genres")
    favorite_games = s.SerializerMethodField(method_name="get_favorite_games")

    class Meta:
        model = User
        fields = ["id", "username", "url", "reviews", "reviews_n",
                  "average_score", "reviews_hist", "favorite_genres",
                  "favorite_games"]

    # Uses obj to generate required data
    def get_reviews_n(self, obj):
        return Review.objects.filter(user=obj).count()
    
    def get_average_score(self, obj):
        return int(Review.objects.filter(user=obj)
                   .aggregate(avg=Avg("score", default=0))["avg"])


    def get_reviews_hist(self, obj):
        reviews = Review.objects.filter(user=obj)
        reviews_hist = [reviews.filter(score__lte=20).count(),
                        reviews.filter(score__gt=20, score__lte=40).count(),
                        reviews.filter(score__gt=40, score__lte=60).count(),
                        reviews.filter(score__gt=60, score__lte=80).count(),
                        reviews.filter(score__gt=80, score__lte=100).count()]
        return reviews_hist
    
    def get_favorite_genres(self, obj):
        reviews = (Review.objects.filter(user=obj)
                   .values("game__genre__name", "score")
                   .annotate(genre_count=Count("game__genre__name"),
                             average_score=Avg("score"))
                   .order_by("-average_score", "-genre_count")[:3])
        genres = [review["game__genre__name"] for review in reviews]
        return genres
    
    def get_favorite_games(self, obj):
        reviews = Review.objects.filter(user=obj).order_by("-score")[:3]
        return ReviewSerializer(
            reviews,
            context={'request': self.context.get("request")},
            many=True, fields=["url", "game", "score"]
            ).data


class ReviewSerializer(DynamicFieldsSerializer):
    """Serializer for a review."""
    user = UserSerializer(fields=['username', 'url'], read_only=True)
    game = GameSerializer(fields=['title', 'url'], read_only=True)

    class Meta:
        model = Review
        fields = ["id", "url", "user", "game", "date", "score", "content"]

    def validate_date(self, date):
        """Validator for review date"""
        if not isinstance(date, datetime.date):
            raise s.ValidationError("Date must be in format datetime.date format YYYY-MM-DD")
        if date > datetime.date.today():
            raise s.ValidationError("Date can not be in the future.")
        return date

    def create(self, validated_data):
        """Used by POST /api/reviews"""
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Used by PATCH /api/reviews/{review__id}"""
        if "score" in validated_data:
            instance.score = validated_data["score"]
        if "content" in validated_data:
            instance.content = validated_data["content"]
        instance.date = instance.date
        instance.save()
        return instance


class GameAnalyticsSerializer(s.Serializer):
    """Serializer for GET /api/games/<game__id>/analytics."""
    game = s.SerializerMethodField(method_name="get_game")
    reviews_n = s.SerializerMethodField(method_name="get_reviews_n")
    average_score = s.SerializerMethodField(method_name="get_average_score")
    reviews_hist = s.SerializerMethodField(method_name="get_reviews_hist")
    best_month = s.SerializerMethodField(method_name="get_best_month")

    def __init__(self, *args, **kwargs):
        """Taken from DynamicFieldsSerializer."""
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    # Processes to generate data for analytics
    def get_game(self, obj):
        return GameSerializer(
            obj,
            context={'request': self.context.get("request")},
            fields=["title", "url"]).data

    def get_reviews_n(self, obj):
        return Review.objects.filter(game=obj).count()

    def get_reviews_hist(self, obj):
        reviews = Review.objects.filter(game=obj)
        reviews_hist = [reviews.filter(score__lte=20).count(),
                        reviews.filter(score__gt=20, score__lte=40).count(),
                        reviews.filter(score__gt=40, score__lte=60).count(),
                        reviews.filter(score__gt=60, score__lte=80).count(),
                        reviews.filter(score__gt=80, score__lte=100).count()]
        return reviews_hist

    def get_average_score(self, obj):
        return int(Review.objects.filter(game=obj)
                   .aggregate(avg=Avg("score", default=0))["avg"])

    def get_best_month(self, obj):
        return (Review.objects.filter(game=obj)
                .values("date")
                .annotate(reviews_n=Count("date"))
                .order_by("-reviews_n").first())


class GamesAnalyticsSerializer(s.Serializer):
    """Serializer for GET /api/games/."""
    top_rated = s.SerializerMethodField(method_name="get_top_rated")
    trending = s.SerializerMethodField(method_name="get_trending")

    # Uses obj to generate analysis data
    def get_top_rated(self, obj):
        games = (obj.annotate(review_n=Count("review"),
                              average_score=Avg("review__score"))
                 .order_by("-average_score", "-review_n")[:5])
        serializer = GameAnalyticsSerializer(
            games, many=True, context={'request': self.context.get("request")},
            fields=["game", "average_score"])
        return serializer.data

    def get_trending(self, obj):
        # Gets 100 most recent reviews from the given games
        recent = (Review.objects.filter(game__title__in=obj.values("title"))
                  .order_by("-date")[:100])
        # Gets games grouped and ordered by the number of recent reviews
        reviews = (Review.objects
                   .filter(id__in=recent.values("id"), game__in=obj)
                   .values("game").order_by("game")
                   .annotate(count=Count("game"))
                   .order_by("-count")[:5])
        games = Game.objects.filter(id__in=reviews.values("game"))

        return GameSerializer(games, many=True,
                              context={'request': self.context.get("request")},
                              fields=["title", "url"]).data
