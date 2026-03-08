from django.contrib import admin
from .models import Recipe, Ingredient, Nutrition, UserIngredients

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Nutrition)
admin.site.register(UserIngredients)
