"""
Unit tests for API methods in fridge_manager.views.
"""
from fridge_manager.views import *
import pytest

class TestApi:
    
    def test_get():
        assert False
        

class TestUsers(TestApi):


class Test
    

GET users/{user_id} = show profile to user (must be logged in)
POST users = sign up
POST users/{user_id} = login
PUT users/{user_id} = update user profile (must be logged in)
DELETE users/{user_id} = delete profile

GET users/{user_id}/fridge = shows ingredients currently in fridge (must be logged in)
PUT users/{user_id}/fridge = update fridge (add or delete ingredients) (must be logged in)\

GET ingredients = show list of all ingredients
GET ingredients/{ingredient_id} = show ingredient information

GET recipes = show list of recipes (ordered by what user has available)
GET recipes/{recipe_id} = show information on specific recipe

PUT recipes/{recipe_id} = update recipe (must only be for author of the recipe)
POST recipes = create new recipe (must be logged in)
DELETE recipes/{recipe_id} = delete recipe