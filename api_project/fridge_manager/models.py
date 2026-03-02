"""
Contains all models for the fridge_manager application.
"""

from django.db import models
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    """Models an ingredient by its name and unit of measurement."""
    name = models.CharField(max_length=30)
    unit = models.IntegerField(null=True, blank=True)


class Recipe(models.Model):
    """
    Models a recipe by its name, author, time to make, description,
    category, instructions, and serving and/or yield size. Has a many-to-many
    relationship with auth.Users to represent the recipes a User has saved.
    
    Recipe categories were collated from the original .csv file the recipes
    were sourced from.
    """
    
    # Extracted from original database recipe categories. Bread = Breads and Yeast Breads and Quick Breads. Cookies = Bar Cookie and Drop Cookies. Dessert = Dessert and Cheesecake
    # Meat = Meat and Poultry, Stocks = Stocks and Clear Soup, Smoothies = Shakes and Smoothies, Stew = Stew + Gumbo
    categories = {"ME": "Meat", "VG": "Vegetable", "FR": "Fruit", "CH": "Cheese",
                  "BE": "Beans", "PO": "Potato", "RI": "Rice", "BR": "Bread",
                  "SA": "Sauces", "CA": "Candy", "PI": "Pie", "DE": "Dessert",
                  "BF": "Breakfast", "LU": "Lunch/Snacks", "SW": "Stew",
                  "CD": "Chowders", "SP": "Spreads", "SD": "Salad Dressings",
                  "SC": "Scones", "CO": "Cookies", "ST": "Stocks",
                  "SM": "Smoothies"}
    
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    time = models.DurationField()
    description = models.TextField(max_length=500, blank=True, default="")
    category = models.CharField(max_length=2, choices=categories)
    instructions = models.TextField(max_length=1000)
    serves = models.IntegerField(validators=[MinValueValidator(0)], null=True,
                                 blank=True)
    yields = models.CharField(max_length = 30, blank=True)
    users = models.ManyToManyField("auth.User", related_name="saved_recipes")


class RecipeIngredients(models.Model):
    """
    Intermediary table that represents the ingredients that belong to a recipe.
    ALso has a field to represent the quantity of an ingredient, which is
    multiplied by Ingredient.unit.
    """
    pk = models.CompositePrimaryKey("recipe_id", "ingredient_id")
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=True, default=1)


class Nutrition(models.Model):
    """
    Model for the nutritional value of a Recipe or Ingredient using its
    calories, total fat, saturated fat, carbohydrates, sugars, protein, sodium,
    and fiber.
    
    Needs to have either an ingredient_id or recipe_id, but not both.
    """
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
    """
    Model to represent the ingredients a User has in their fridge or grocery
    list; the boolean field 'fridge' is used to determine which one.
    """
    user = models.ForeignKey("auth.User", related_name="ingredients",
                             on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    fridge = models.BooleanField(default=True)
