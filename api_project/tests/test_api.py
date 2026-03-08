"""
Unit tests for API methods in games.views.
"""
import pytest
from games import views


class TestUsers:
    """
    Tests for API endpoints on users: POST users, GET users/{user_id},
    PUT users/{user_id}, DELETE users/{user_id}, and GET users/{user_id}/recipes.
    
    Also tests authentication using Django's auth.User model.
    """
        
    @pytest.mark.parametrize("password", ["validpassword", "tooshort", "546123457853245"])
    def test_post_passwords(self, password):
        """
        Tests POST users by signing up with a valid username and a variety of passwords,
        in order of:
        a valid password, a password that is too short, password that is numeric.
        
        Passes when first password is successful and returns a 201 HTTP Created,
        and the rest return HTTP 400 Bad Request errors.
        """
        # Remember to check that the user does not exist beforehand (for first test)
        assert False
    
    def test_post_username_taken(self):
        """
        Tests POST users by signing up with a username that is not unique.
        
        Passes when it returns a HTTP 409 Conflict error.
        """
        assert False
    
    def test_authentication(self):
        """
        Tests logging in with a valid username and password.
        
        Passes when it returns a HTTP 200 OK.
        """
        # Login with valid credentials using fixture, check that it was successful (auth.get_user)
        assert False
    
    @pytest.mark.parametrize("user_id", [1, 0])
    def test_get_id_valid(self, user_id):
        """
        Tests GET users/{user_id} on a valid and invalid user_id
        
        Passes when the first returns a correct user information and a HTTP 200 OK,
        and the second returns a HTTP 404 Not Found error.
        """
        assert False
    
    @pytest.mark.parametrize("user_id", [1, 2, 0, -1])
    def test_put_id(self, user_id):
        """
        Tests PUT users/{user_id} for an authenticated user on their own user_id,
        someone else's user_id, for an unauthenticated user, and an invalid id.
        
        Passes when the first commits changes successfully with a HTTP 200 OK,
        the second returns a HTTP 403 Forbidden error, the third returns a 401
        Unauthorized error, and the fourth returns a HTTP 404 Not Found error.
        """
        assert False
        
    @pytest.mark.parametrize("user_id", [2, 3, 0, -1])
    def test_delete_id(self, user_id):
        """
        Tests DELETE users/{user_id} for an authenticated user on their own user_id
        and someone else's user_id, for an unauthenticated user, and for an invalid
        user_id.
        
        Passes when the first successfully deletes a user and returns a HTTP
        200 OK, the second returns a HTTP 403 Forbidden error, the third
        returns a HTTP 401 Unauthorized error, and the fourth returns a HTTP 404
        Not Found error.
        """
        assert False
    
    @pytest.mark.parametrize("user_id", [2, 3, 0, -1])
    def test_get_id_recipes(self, user_id):
        """
        Tests GET users/{user_id}/recipes for an authenticated user on their own user_id
        and someone else's user_id, for an unauthenticated user, and for an invalid
        user_id.
        
        Passes when the first successfully deletes a user and returns a HTTP
        200 OK, the second returns a HTTP 403 Forbidden error, the third
        returns a HTTP 401 Unauthorized error, and the fourth returns a HTTP 404
        Not Found error.
        """
        assert False


@pytest.mark.parametrize("ingredient_id", [1, -1])
def test_get_id(ingredient_id):
    """
    Tests GET ingredients/{ingredient_id} with a valid and invalid
    ingredient_id.
    
    Passes when the first returns correct data and a HTTP 200 OK, and the
    second returns a HTTP 404 Not Found error.
    """
    assert False


class TestRecipes:
    """
    Tests for API endpoints on recipes: GET recipes, GET recipes?{parameter}={value},
    GET recipes/{recipe_id}.
    """
    
    def test_get_unauthenticated(self):
        """
        Tests GET recipes for an unauthenticated user.
        
        Passes when it returns correct data and a HTTP 200 OK.
        """
        assert False
    
    def test_get_authenticated(self):
        """
        Tests GET recipes for an authenticated user.
        
        Passes when it returns correct data (personalised recommendations)
        and a HTTP 200 OK.
        """
        assert False
    
    @pytest.mark.parametrize("parameter, value", [("category", "Dessert"),
                                                  ("category", "NotACategory"),
                                                  ("author", "Dancer"),
                                                  ("author", "NotAnAuthor")])
    def test_get_filtered(self, parameter, value):
        """
        Tests GET recipes?{parameter}={value} for recipes filtered by a specific
        category or author.
        
        There is one valid test for each parameter that should return correct
        data and a HTTP 200 OK, and the other two tests return a HTTP 404 Not
        Found error.
        """
        assert False
    
    @pytest.mark.parametrize("recipe_id", [1, -1])
    def test_get_id(self, recipe_id):
        """
        Tests GET recipe/{recipe_id} with a valid and invalid recipe_id.
        
        Passes when the first returns correct data and a HTTP 200 OK, and the
        second returns a HTTP 404 Not Found error.
        """
        assert False
    
    def test_get_id_authenticated(self):
        """
        Tests GET recipe/{recipe_id} for an authenticated user.
        
        Passes if there is an appropriate link to save the recipe for the user.
        """
        assert False
    

class TestUserIngredients:
    """
    Tests for API endpoints on a user's fridge and grocery list:
    GET users/{user_id}/fridge, PUT users/{user_id}/fridge/{ingredient_id},
    DELETE users/{user_id}/fridge/{ingredient_id}, GET users/{user_id}/grocery,
    PUT users/{user_id}/grocery/{ingredient_id},
    DELETE users/{user_id}/grocery/{ingredient_id}.
    """
    test_parameters = [("fridge", 1), ("fridge", 2), ("fridge", 0), ("fridge", -1),
                       ("grocery", 1), ("grocery", 2), ("grocery", 0),
                       ("grocery", -1)]
    
    @pytest.mark.parametrize("function, user_id", test_parameters)
    def test_get_users_id(self, function, user_id):
        """
        Tests GET users/{user_id}/fridge and GET users/{user_id}/grocery
        for a user on their own fridge/grocery and on another user's fridge/grocery,
        an invalid user_id, and an unauthenticated user.
        
        Passes when the first scenarios return correct data and a HTTP
        200 OK, the second returns a HTTP 403 Forbidden error, the third a HTTP
        404 Not Found error, and the fourth returns a HTTP 401 Unauthorized error.
        """
        assert False
        
    @pytest.mark.parametrize("function, user_id", test_parameters)
    def test_put_users_id(self, function, user_id):
        """
        Tests PUT users/{user_id}/fridge/{ingredient_id} and
        PUT users/{user_id}/grocery/{ingredient_id} for a user by adding an
        ingredient to their own fridge/grocery and to another user's fridge/grocery,
        and for an unauthenticated user.
        
        Passes when the first scenarios return correct data and a HTTP
        201 Created, the second returns a HTTP 403 Forbidden error, the third a
        HTTP 404 Not Found error, and the fourth returns a HTTP 401 Unauthorized
        error.
        """
        assert False
    
    
    def test_put_users_id_reduce(self):
        """
        Tests PUT users/{user_id}/fridge and PUT users/{user_id}/grocery for
        reducing a quantity of an ingredient in a fridge/grocery.
        
        Passes when changes are committed successfully and it returns a HTTP
        200 OK.
        """
        assert False

    @pytest.mark.parametrize("function, user_id", test_parameters)
    def test_delete_users_id(self, function, user_id):
        """
        Tests DELETE users/{user_id}/fridge/{ingredient_id} and
        DELETE users/{user_id}/grocery/{ingredient_id} for a user on their own
        fridge/grocery and another user's fridge/grocery, and for an
        unauthenticated user.
        
        Passes when the first scenarios delete successfully and return a HTTP
        200 OK, the second returns a HTTP 403 Forbidden error, the third a HTTP
        404 Not Found error, and the fourth returns a HTTP 401 Unauthorized error.
        """
        assert False
