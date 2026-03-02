from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
    
class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    unit = models.IntegerField(null=True, blank=True)

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey("auth.User", related_name="recipes",
                               on_delete=models.CASCADE)
    time = models.DurationField()
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=30)
    instructions = models.TextField(max_length=1000)
    serves = models.IntegerField(validators=[MinValueValidator(0)], null=True,
                                 blank=True)
    yields = models.CharField(max_length = 30, blank=True)

class RecipeIngredients(models.Model):
    pk = models.CompositePrimaryKey("recipe_id", "ingredient_id")
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=True, default=1)
    
class Nutrition(models.Model):
    ingredient_id = models.ForeignKey(Ingredient, null=True,
                                      on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
    kcal = models.FloatField(null=True, blank=True,
                             validators=[MinValueValidator(0)])
    total_fat = models.FloatField(null=True, blank=True,
                             validators=[MinValueValidator(0)])
    saturated_fat = models.FloatField(null=True, blank=True,
                             validators=[MinValueValidator(0)])
    carbs = models.FloatField(null=True, blank=True,
                             validators=[MinValueValidator(0)])
    sugars = models.FloatField(null=True, blank=True,
                             validators=[MinValueValidator(0)])
    protein = models.FloatField(null=True, blank=True,
                             validators=[MinValueValidator(0)])
    sodium = models.FloatField(null=True, blank=True,
                             validators=[MinValueValidator(0)])
    fiber = models.FloatField(null=True, blank=True,
                             validators=[MinValueValidator(0)])
    
class UserIngredients(models.Model):
    user = models.ForeignKey("auth.User", related_name="ingredients",
                             on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    fridge = models.BooleanField(default=True)

