"""Contains all models for the games application."""

import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Genre(models.Model):
    """Models a videogame genre."""
    name = models.CharField(max_length=30, unique=True)


class Platform(models.Model):
    """Models a videogame platform."""
    name = models.CharField(max_length=30, unique=True)


class Developer(models.Model):
    """Models a videogame developer."""
    name = models.CharField(max_length = 30, unique=True)


class Publisher(models.Model):
    """Models a videogame publisher."""
    name = models.CharField(max_length=30, unique=True)


class Game(models.Model):
    """Models a videogame."""
    ratings = {"AO": "Adult Only", "E": "Everyone", "E10+": "Everyone 10+",
               "K-A": "Kids to Adults", "M": "Mature", "RP": "Rating Pending",
               "T": "Teen"}

    title = models.CharField(max_length=50)
    release_date = models.DateField(null=True, blank=True)
    rating = models.CharField(choices=ratings, blank=True)
    description = models.TextField(blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    platforms = models.ManyToManyField(Platform, related_name="games")
    developers = models.ManyToManyField(Developer, related_name="games")
    publishers = models.ManyToManyField(Publisher, related_name="games")


    class Meta:
        ordering = ["-release_date"]

    # Overrides save method to validate date (cannot be in the future).
    def save(self, *args, **kwargs):
        if isinstance(self.release_date, str) or self.release_date is None:
            self.release_date = None
        elif self.release_date > datetime.date.today():
            raise ValidationError("The date cannot be in the future.")
        super(Game, self).save(*args, **kwargs)


class Review(models.Model):
    """Models a user's review for a specfic videogame."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    score = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(100)])
    content = models.TextField(max_length=1000)

    class Meta:
        ordering = ["-date"]

    # Overrides save method to validate date.
    def save(self, *args, **kwargs):
        if self.date > datetime.date.today():
            raise ValidationError("The date cannot be in the future.")
        super(Review, self).save(*args, **kwargs)
