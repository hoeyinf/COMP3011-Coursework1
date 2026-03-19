"""
Contains serializers that allow for easier serialization and deserialization of data into JSON
for API calls.
"""
import datetime
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

    class Meta:
        model = User
        fields = ["id", "username", "url", "reviews", "reviews_n",
                  "average_review_score", "reviews_hist"]

    def get_reviews_hist(self, obj):
        return self.context.get("reviews_hist")
        



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
