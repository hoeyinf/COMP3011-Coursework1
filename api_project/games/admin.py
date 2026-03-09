from django.contrib import admin
from .models import Game, Genre, Review, Platform, Developer, Publisher


# Register your models here.
admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Platform)
admin.site.register(Developer)
admin.site.register(Publisher)
