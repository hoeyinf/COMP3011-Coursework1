"""
Contains serializers that allow for easier serialization and deserialization of data into JSON
for API calls.
"""

from rest_framework import serializers as s
from django.contrib.auth.models import User
from games.models import Game, Review, Genre, Platform, Developer, Publisher, User

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


class GenreSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Genre
        fields = ["name", "url"]


class PlatformSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Platform
        fields = ["name", "url"]


class DeveloperSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Developer
        fields = ["name", "url"]


class PublisherSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Publisher
        fields = ["name", "url"]


class GameSerializer(DynamicFieldsSerializer):
    """Serializer for a Game."""
    genre = GenreSerializer(read_only=True)
    platforms = PlatformSerializer(many=True, read_only=True)
    developers = DeveloperSerializer(many=True, read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    reviews = s.HyperlinkedIdentityField(view_name='game-reviews')
    class Meta:
        model = Game
        fields = ["id", "title", "url", "release_date", "rating", "description",
                  "genre", "platforms", "developers", "publishers", "reviews"]


class UserSerializer(DynamicFieldsSerializer):
    """Serializer for a User."""
    reviews = s.HyperlinkedIdentityField(view_name='user-reviews')
    class Meta:
        model = User
        fields = ["id", "username", "url", "reviews"]


class ReviewSerializer(DynamicFieldsSerializer):
    """Serializer for a User's Review of a Game."""
    user = UserSerializer(fields=['username', 'url'])
    game = GameSerializer(fields=['title', 'url'])
    class Meta:
        model = Review
        fields = ["id", "url", "user", "game", "date", "score", "content"]
