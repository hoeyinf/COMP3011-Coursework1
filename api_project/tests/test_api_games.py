"""Unit tests for API methods regarding games: /api/games/"""
import pytest
import requests

INVALID_ID = 0

class TestGamesId:
    """
    Tests API endpoints GET /api/games/, including the use of query
    parameters.
    """
    
    @pytest.fixture(autouse=True)
    def set_fixtures(self, server, existing_review, existing_game):
        """Sets fixures so that they can be called using self."""
        self.server = server
        self.existing_review = existing_review
        self.existing_game = existing_game

    def test_get(self):
        """
        Tests GET /api/games/.

        Passes when it returns the correct number of games and a HTTP 200 OK.
        """
        r = requests.get(f"{self.server}api/games/")
            
        assert len(r.json()) == 25 and r.status_code == 200

    @pytest.mark.parametrize("game_id, response", [("existing_game", 200),
                                                   (INVALID_ID, 404),
                                                   ("", 200)])
    def test_get_id(self, game_id, response):
        """
        Tests GET /api/games/<game__id>

        Passes when:
        - Valid game_id returns correct data and a HTTP 200 OK.
        - Invalid game_id returns a HTTP 404 Not Found.
        - No game_id returns the same response as GET /api/games/ and a HTTP 200
        OK
        """
        if game_id == "existing_game": game_id = self.existing_game["id"]

        r = requests.get(f"{self.server}api/games/{game_id}")

        # Checks that game data matches fixture for relevant test
        if game_id == self.existing_game["id"]:
            assert all(r.json()[key] == self.existing_game[key]
                       for key in self.existing_game)
        # Checks that missing game_id matches the correct API endpoint
        # Yes this is kind of pointless. It's the exact same request.
        elif game_id == "":
            games = requests.get(f"{self.server}api/games/")
            assert r.json() == games.json()

        assert r.status_code == response

    @pytest.mark.parametrize("game_id, response", [("existing_game", 200),
                                                   (INVALID_ID, 404)])
    def test_get_id_analytics(self, game_id, response):
        """
        Tests GET /api/games/<game__id>/analytics for valid and invalid game_id
        for correct HTTP responses.

        Passes when:
        - Valid game_id returns correct data and a HTTP 200 OK.
        - Invalid game_id returns an HTTP 404 Not Found.
        """
        if game_id == "existing_game": game_id = self.existing_game["id"]

        r = requests.get(f"{self.server}api/games/{game_id}/analytics")

        assert r.status_code == response

    @pytest.mark.parametrize("game_id, response", [("existing_game", 200),
                                                   (INVALID_ID, 404)])
    def test_get_reviews(self, game_id, response):
        """
        Tests GET /api/games/<game__id>/reviews/ for a valid and invalid game_id.
        
        Passes when:
        - Valid game_id returns a matching review and a HTTP 200 OK.
        - Invalid game_id returns a HTTP 404 Not Found.
        """
        if game_id == "existing_game": game_id = self.existing_game["id"]

        r = requests.get(f"{self.server}api/games/{game_id}/reviews/")

        # Checks that the response contains the fixture for a successful GET
        if response == 200:
            for review in r.json():
                if review["id"] == self.existing_review["id"]:
                    for key in self.existing_review:
                        assert review[key] == self.existing_review[key]
                break

        assert r.status_code == response

    @pytest.mark.parametrize("category, value", [("genre", "action"),
                                                 ("platform", "pc"),
                                                 ("developer", "ea games"),
                                                 ("publisher", "nintendo"),
                                                 ("page", "5"),
                                                 ("name", "disco"),
                                                 ("idonotexist", "meeither"),
                                                 (["genre", "platform"],
                                                  ["action", "pc"])])
    def test_category(self, category, value):
        """
        Tests GET /api/games/?category=value. Values must be case-insensitive.

        Passes when:
        - They each return a HTTP 200 OK.
        - Non-existent category returns a HTTP 404 Not Found.
        """
        # Sets params based on test conditions
        params = {}
        if isinstance(category, list):
            for i in range(len(category)):
                params[category[i]] = value[i]
        else: params = {f"{category}": value}

        r = requests.get(f"{self.server}api/games/", params=params)
        
        # Check that every category is listing all its relevant data
        response = 200
        if category == "idonotexist": response = 404
        
        assert r.status_code == response

def test_method_not_allowed(server):
    """
    Tests POST /api/games/

    Passes when it returns a HTTP 405 Method Not Allowed.
    """
    # Need to authenticate here
    r = requests.post(f"{server}api/games/")
    assert r.status_code == 405, f"Expected = 405. Response = {r.status_code}."
