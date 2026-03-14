"""
Contains serializers that allow for easier serialization and deserialization of data into JSON
for API calls.
"""

from rest_framework import serializers as s
from django.contrib.auth.models import User
from games.models import Game, Review, Genre, Platform, Developer, Publisher, User

class CategorySerializer(s.ModelSerializer):
    # Each category should show its own url so that it shows up in the nested serialization
    class Meta:
        fields = ["id", "name"]


class GenreSerializer(CategorySerializer):
    uri = s.HyperlinkedIdentityField(view_name="genre-detail")
    class Meta:
        model = Genre


class PlatformSerializer(CategorySerializer):
    uri = s.HyperlinkedIdentityField(view_name="platform-detail")
    class Meta:
        model = Platform


class DeveloperSerializer(CategorySerializer):
    uri = s.HyperlinkedIdentityField(view_name="developer-detail")
    class Meta:
        model = Developer


class PublisherSerializer(CategorySerializer):
    uri = s.HyperlinkedIdentityField(view_name="publisher-detail")
    class Meta:
        model = Publisher


class GameSerializer(s.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    platforms = PlatformSerializer(many=True, read_only=True)
    developers = DeveloperSerializer(many=True, read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    reviews = s.HyperlinkedRelatedField(many=True, read_only=True, view_name='')
    # Needs a url so that it shows up in nested serialization
    class Meta:
        model = Game
        fields = ["id", "title", "release_date", "rating", "description",
                  "genre", "platforms", "developers", "publishers", "reviews"]


class ReviewSerializer(s.ModelSerializer):
    user = s.SlugRelatedField(queryset=User.objects.all(),
                              slug_field="username")
    game = s.SlugRelatedField(queryset=Game.objects.all(), slug_field="title")
    # Does not need a url. All other serializers should use HyperlinkedRelatedField
    class Meta:
        model = Review
        fields = ["id", "user", "game", "date", "score", "content"]


class UserSerializer(s.ModelSerializer):
    # Needs a url so that it shows up in nested serialization (REVIEWS)
    class Meta:
        model = User
        fields = ["id", "username"]
