from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Game, Genre, Review, Platform, Developer, Publisher, User


# Register your models here.
admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Platform)
admin.site.register(Developer)
admin.site.register(Publisher)
admin.site.register(User, UserAdmin)
