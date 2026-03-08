"""
Unit tests for API methods in games.views.
"""
import pytest
from games import views

VALID_USER_ID = 1
INVALID_USER_ID = 0
VALID_GAME_ID = 1
INVALID_GAME_ID = 0

class TestUsers:
    """
    Tests signup and login via Django's provided User model, as well as the
    GET /users/{user_id} API endpoint.
    """
        
    @pytest.mark.parametrize("password", ["validpassword",
                                          "tooshort",
                                          "546123457853245"])
    def test_post_passwords(self, password):
        """
        Tests user sign up using:
        valid password, password that is too short, password that is numeric.
        
        Passes when:
        - Valid password succeeds and returns a 201 HTTP Created.
        - Invalid passwords return a HTTP 400 Bad Request.
        """
        # Remember to check that the user does not exist beforehand (for first test)
        assert False
    
    def test_post_username_taken(self):
        """
        Tests user sign up using a username that is not unique.
        
        Passes when it returns a HTTP 409 Conflict.
        """
        assert False
    
    def test_authentication(self):
        """
        Tests logging in with a valid username and password.
        
        Passes when it returns a HTTP 200 OK.
        """
        # Login with valid credentials using fixture, check that it was successful (auth.get_user)
        assert False
    
    @pytest.mark.parametrize("user_id", [VALID_USER_ID, INVALID_USER_ID])
    def test_get(self, user_id):
        """
        Tests GET /users/{user_id} on a valid and invalid user_id
        
        Passes when:
        - Valid user_id returns correct user information and a HTTP 200 OK.
        - Invalid user_id returns a HTTP 404 Not Found.
        """
        assert False


class TestReviews:
    """
    Tests API endpoints for reviews:
    - GET /games/{game_id}/reviews
    - GET /games/{game_id}/reviews/{user_id}
    - POST /games/{game_id}/reviews
    - PUT /games/{game_id}/reviews/{user_id}
    - DELETE /games/{game_id}/reviews/{user_id}
    """
    
    @pytest.mark.parametrize("game_id", [VALID_GAME_ID, INVALID_GAME_ID])
    def test_get(self, game_id):
        """
        Tests GET /games/{game_id}/reviews for a valid and invalid game_id.
        
        Passes when:
        - Valid game_id returns correct reviews and a HTTP 200 OK.
        - Invalid game_id returns a HTTP 404 Not Found.
        """
        assert False

    @pytest.mark.parametrize("game_id,user_id", [(VALID_GAME_ID, VALID_USER_ID),
                                                 (VALID_GAME_ID, INVALID_USER_ID),
                                                 (INVALID_GAME_ID, VALID_USER_ID)])
    def test_get_id(self, game_id, user_id):
        """
        Tests GET /games/{game_id}/reviews/{user_id} for a variety of
        valid and invalid game_ids and user_ids.
        
        Passes when:
        - Valid IDs return the correct reviews and a HTTP 200 OK.
        - Invalid IDs return a HTTP 404 Not Found.
        """
        assert False
    
    def test_get_own_id(self):
        """
        Tests GET /games/{game_id}/reviews/{user_id} for a user on their own
        review.

        Passes when it also provides a link to edit the review and returns a
        HTTP 200 OK.
        """
        assert False

    @pytest.mark.parametrize("game_id,authenticated", [(VALID_GAME_ID, True),
                                                       (VALID_GAME_ID, False),
                                                       (INVALID_GAME_ID, True)])
    def test_post(self, game_id, authenticated):
       """
       Tests POST /games/{game_id}/reviews for valid and invalid game_ids on
       authenticated and unauthenticated users.

       Passes when:
       - Valid game_id and authenticated user creates a new review and returns a
         201 HTTP Created.
       - Unauthenticated user returns a HTTP 401 Unauthorized.
       - Invalid game_id returns a HTTP 404 Not Found.
       """
       assert False

    def test_post_existing(self):
        """
        Tests POST /games/{game_id}/reviews when the user has an existing
        review for that game.

        Passes when it returns a HTTP 409 Conflict.
        """
        assert False

    @pytest.mark.parametrize("game_id,authenticated", [(VALID_GAME_ID, True),
                                                       (VALID_GAME_ID, False),
                                                       (INVALID_GAME_ID, True)])
    def test_put(self, game_id, authenticated):
        """
        Tests PUT /games/{game_id}/reviews/{user_id} for valid and invalid
        game_ids on authenticated and unauthenticated users.

        Passes when:
        - Valid game_id and authenticated user updates the correct review and
        returns a HTTP 200 OK.
        - Unauthenticated user returns a HTTP 401 Unauthorized.
        - Invalid game_id returns a HTTP 404 Not Found.
        """
        assert False

    def test_put_forbidden(self):
        """
        Tests POST /games/{game_id}/reviews/{user_id} for a user trying to
        update another user's review.

        Passes when it returns a HTTP 403 Forbidden.
        """
        assert False

    def test_put_nonexisting(self):
        """
        Tests POST /games/{game_id}/reviews/{user_id} for a user's nonexistent
        review.

        Passes when it returns a HTTP 404 Not Found.
        """
        assert False

    @pytest.mark.parametrize("existent,own", [(True, True), (False, True),
                                              (True, False)])
    def test_delete(self, existent, own):
        """
        TESTS DELETE /games/{game_id}/reviews/{user_id} for an existent review,
        non-existent review, and another user's review.

        Passes when:
        - Existent review is deleted and returns a HTTP 200 OK.
        - Nonexistent review returns a HTTP 404 Not Found.
        - Another user's review returns a HTTP 403 Forbidden.
        """
        assert False

    def test_delete_unauthenticated(self):
        """
        TESTS DELETE /games/{game_id}/reviews/{user_id} for an unauthenticated
        user.
        
        Passes when it returns a HTTP 401 Unauthorized.
        """
        assert False


class TestGamesId:
    """
    Tests API endpoints for games/{game_id} (excluding game reviews):
    - GET /games
    - GET /games/{game_id}
    - GET /games/{game_id}/analytics
    """

    def test_get(self):
        """
        Tests GET /games.

        Passes when it returns correct data and a HTTP 200 OK.
        """
        assert False

    @pytest.mark.parametrize("game_id", [VALID_GAME_ID, INVALID_GAME_ID])
    def test_get_id(self, game_id):
        """
        Tests GET /games/{game_id} for valid and invalid game_id.

        Passes when:
        - Valid game_id returns correct data and a HTTP 200 OK.
        - Invalid game_id returns an HTTP 404 Not Found.
        """
        assert False

    @pytest.mark.parametrize("game_id", [VALID_GAME_ID, INVALID_GAME_ID])
    def test_get_id_analytics(self, game_id):
        """
        Tests GET /games/{game_id}/amalytics for valid and invalid game_id.

        Passes when:
        - Valid game_id returns correct data and a HTTP 200 OK.
        - Invalid game_id returns an HTTP 404 Not Found.
        """
        assert False


class TestGamesCategories:
    """
    Tests API endpoints for different game categories:
    - GET /games/genres
    - GET /games/genres/{genre_id}
    - GET /games/platforms
    - GET /games/platforms/{platform_id}
    - GET /games/developers
    - GET /games/developers/{developer_id}
    - GET /games/publishers
    - GET /games/publishers/{publisher_id}
    """

    @pytest.mark.parametrize("category", ["genres", "platforms", "developers",
                                          "publishers", "idonotexist"])
    def test_category(self, category):
        """
        Tests the 4 API endpoints with the structure GET /games/{category}.

        Passes when:
        - They each return the correct data and a HTTP 200 OK.
        - Non-existent category returns a HTTP 404 Not Found.
        """
        assert False

    @pytest.mark.parametrize("category", ["genres", "platforms", "developers",
                                          "publishers"])
    def test_category_id_valid(self, category):
        """
        Tests the 4 API endpoints with the structure
        GET /games/{category}/{category_id}, with valid category_ids.

        Passes when they each return the correct data and a HTTP 200 OK.
        """
        assert False

    @pytest.mark.parametrize("category", ["genres", "platforms", "developers",
                                          "publishers"])
    def test_category_id_invalid(self, category):
        """
        Tests the 4 API endpoints with the structure
        GET /games/{category}/{category_id}, with invalid category_ids.

        Passes when they each return a HTTP 404 Not Found.
        """
        assert False


def test_method_not_allowed():
    """
    Tests POST /games.

    Passes when it returns a HTTP 405 Method Not Allowed.
    """
    assert False


def test_not_implemented():
    """
    Tests HEAD /games

    Passes when it returns a HTTP 501 Not Implemented.
    """
    assert False
