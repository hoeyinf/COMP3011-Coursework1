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
    reviews_n = s.IntegerField()
    
    class Meta:
        model = Game
        fields = ["id", "title", "url", "release_date", "rating", "description",
                  "genre", "platforms", "developers", "publishers","reviews",
                  "reviews_n"]


class UserSerializer(DynamicFieldsSerializer):
    """Serializer for a user."""

    reviews = s.HyperlinkedIdentityField(view_name='user-reviews')
    reviews_n = s.IntegerField()
    average_review_score = s.IntegerField()
    reviews_hist = s.SerializerMethodField(method_name="get_reviews_hist")
    recent_reviews = s.SerializerMethodField(method_name="get_recent_reviews")
    favorite_genres = s.SerializerMethodField(method_name="get_favorite_genres")
    favorite_games = s.SerializerMethodField(method_name="get_favorite_games")

    class Meta:
        model = User
        fields = ["id", "username", "url", "reviews", "reviews_n",
                  "average_review_score", "reviews_hist", "recent_reviews",
                  "favorite_genres", "favorite_games"]

    # Getters for fields below
    def get_reviews_hist(self, obj):
        reviews = self.context.get("reviews")
        reviews_hist = [reviews.filter(score__lte=20).count(),
                        reviews.filter(score__gt=20, score__lte=40).count(),
                        reviews.filter(score__gt=40, score__lte=60).count(),
                        reviews.filter(score__gt=60, score__lte=80).count(),
                        reviews.filter(score__gt=80, score__lte=100).count()]
        return reviews_hist

    def get_recent_reviews(self, obj):
        reviews = self.context.get("reviews").order_by("-date")[:3]
        return ReviewSerializer(
            reviews,
            context={'request': self.context.get("request")},
            many=True, fields=["url", "game", "score", "date"]
            ).data
    
    def get_favorite_genres(self, obj):
        reviews = (self.context.get("reviews")
                   .values("game__genre__name")
                   .annotate(genre_count=Count("game__genre__name"))
                   .order_by("-genre_count")[:3])
        genres = [review["game__genre__name"] for review in reviews]
        return genres
    
    def get_favorite_games(self, obj):
        reviews = self.context.get("reviews").order_by("-score")[:3]
        return ReviewSerializer(
            reviews,
            context={'request': self.context.get("request")},
            many=True, fields=["game", "score"]
            ).data


class ReviewSerializer(DynamicFieldsSerializer):
    """Serializer for a review."""
    user = UserSerializer(fields=['username', 'url'], read_only=True)
    game = GameSerializer(fields=['title', 'url'], read_only=True)

    class Meta:
        model = Review
        fields = ["id", "url", "user", "game", "date", "score", "content"]
        read_only_fields = ["id", "url"]

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
