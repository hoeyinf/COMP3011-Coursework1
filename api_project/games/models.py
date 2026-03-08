"""Contains all models for the games application."""

import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Genre(models.Model):
    """Models a videogame genre."""
    name = models.CharField(max_length=30)


class Game(models.Model):
    """Models a videogame."""
    ratings = {"AO", "E", "E10+", "K-A", "M", "RP", "T"}

    title = models.CharField(max_length=50)
    release_date = models.DateField(null=True, blank=True)
    rating = models.CharField(choices=ratings, blank=True)
    description = models.TextField(blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
    # Overrides save method to validate date (cannot be in the future).
    def save(self, *args, **kwargs):
        if self.date > datetime.date.today():
            raise ValidationError("The date cannot be in the future.")
        super(Game, self).save(*args, **kwargs)


class Review(models.Model):
    """Models a user's review for a specfic videogame."""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000)
    score = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(100)])

    # Overrides save method to validate date.
    def save(self, *args, **kwargs):
        if self.date != datetime.date.today():
            raise ValidationError("The date must be today.")
        super(Game, self).save(*args, **kwargs)


class Platform(models.Model):
    """Models a videogame platform."""
    name = models.CharField(max_length=30)
    games = models.ManyToManyField(Game, related_name="platforms")


class Developer(models.Model):
    """Models a videogame developer."""
    name = models.CharField(max_length = 30)
    games = models.ManyToManyField(Game, related_name="developers")


class Publisher(models.Model):
    """Models a videogame publisher."""
    name = models.CharField(max_length=30)
    games = models.ManyToManyField(Game, related_name="publishers")
