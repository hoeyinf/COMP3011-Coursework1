"""
Contains serializers that allow for easier serialization and deserialization of data into JSON
for API calls.
"""

from rest_framework import serializers as s
from django.contrib.auth.models import User
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
                  "genre", "platforms", "developers", "publishers", "reviews",
                  "reviews_n"]
    """
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews_n'] = instance.reviews.count()
        return representation
    """


class UserSerializer(DynamicFieldsSerializer):
    """Serializer for a user."""
    reviews = s.HyperlinkedIdentityField(view_name='user-reviews')
    class Meta:
        model = User
        fields = ["id", "username", "url", "reviews"]


class ReviewSerializer(DynamicFieldsSerializer):
    """Serializer for a review."""
    user = UserSerializer(fields=['username', 'url'])
    game = GameSerializer(fields=['title', 'url'])
    class Meta:
        model = Review
        fields = ["id", "url", "user", "game", "date", "score", "content"]
