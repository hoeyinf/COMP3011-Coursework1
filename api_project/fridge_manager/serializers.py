from rest_framework import serializers
from fridge_manager.models import Recipe, Ingredient, RecipeIngredients, Nutrition, UserIngredients
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Recipe.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "recipes"]


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    
    class Meta:
        model = Recipe
        fields = ["id", "name", "author", "time", "description", "category",
                  "instructions", "serves", "yields"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "unit"]


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredients
        fields = ["recipe_id", "ingredient_id", "quantity"]


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = ["ingredient_id", "recipe_id", "kcal", "total_fat", "saturated_fat",
                  "carbs", "sugars", "protein", "sodium", "fiber"]

  
class UserIngredientsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model = UserIngredients
        fields = ["user", "ingredient_id", "quantity", "fridge"]
