"""Unit tests for API methods regarding games."""
import pytest
import requests
from games.models import *

VALID_GAME_ID = 1
INVALID_GAME_ID = 0
SERVER = "http://127.0.0.1:8000/"


@pytest.mark.django_db
class TestGamesId:
    """
    Tests API endpoints GET /api/games/, including the use of query
    parameters.
    """

    def test_get(self):
        """
        Tests GET /api/games/.

        Passes when it returns the correct data and a HTTP 200 OK.
        """
        r = requests.get(f'{SERVER}api/games/')
        games = Game.objects.all().order_by('-release_date')
        # Compare the results for the first 20 games
        correct = True
        for i, game in enumerate(games):
            if r.json()[i]['title'] != game.title:
                correct = False
                break
            if i == 20: break
            
        assert correct and r.status_code == 200

    @pytest.mark.parametrize("game_id, response", [(VALID_GAME_ID, 200),
                                                   (INVALID_GAME_ID, 404)])
    def test_get_id_correct_http(self, game_id, response):
        """
        Tests GET /api/games/<game__id> for valid and invalid game_id for correct
        HTTP responses.

        Passes when:
        - Valid game_id returns correct data and a HTTP 200 OK.
        - Invalid game_id returns an HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/games/{game_id}')
        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    def test_get_id_correct_data(self):
        """
        Tests GET /api/games/<game__id> on a valid game_id.

        Passes when it returns the correct data.
        """
        r = requests.get(f'{SERVER}api/games/{VALID_GAME_ID}')
        game = Game.objects.get(pk=VALID_GAME_ID)
        assert (r.json()['title'] == game.title and
                'reviews' in r.json())
        
    def test_get_id_authenticated(self):
        """
        Tests GET /api/games/<game__id> for an authenticated user.

        Passes when it the response contains a link to post a review of the game.
        """
        r = requests.get(f'{SERVER}api/games/{VALID_GAME_ID}')
        assert 'post_review' in r.json()

    @pytest.mark.parametrize("game_id, response", [(VALID_GAME_ID, 200),
                                                   (INVALID_GAME_ID, 404)])
    def test_get_id_analytics_correct_http(self, game_id, response):
        """
        Tests GET /api/games/<game__id>/analytics for valid and invalid game_id
        for correct HTTP responses.

        Passes when:
        - Valid game_id returns correct data and a HTTP 200 OK.
        - Invalid game_id returns an HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/games/{game_id}/analytics')
        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    @pytest.mark.parametrize("game_id, response", [(VALID_GAME_ID, 200),
                                                   (INVALID_GAME_ID, 404)])
    def test_get_reviews_correct_http(self, game_id, response):
        """
        Tests GET /api/games/<game__id>/reviews/ for a valid and invalid game_id.
        
        Passes when:
        - Valid game_id returns correct reviews and a HTTP 200 OK.
        - Invalid game_id returns a HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/games/{game_id}/reviews/')
        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    def test_get_reviews_correct_data(self):
        """
        Tests GET /api/games/<game__id>/reviews/ for a valid game_id.
        
        Passes when the correct data is returned.
        """
        r = requests.get(f'{SERVER}api/games/{VALID_GAME_ID}/reviews/')
        reviews = Review.objects.filter(game=VALID_GAME_ID).order_by('-date')
        # Compares the first 10 reviews to check they match
        correct = []
        for i, review in enumerate(reviews):
            correct.append(r.json()[i]['user']['username'] == review.user.username and
                           r.json()[i]['game']['title'] == review.game.title and
                           r.json()[i]['date'] == str(review.date) and
                           r.json()[i]['score'] == review.score)
            if i == 10: break
            
        assert all(correct)


@pytest.mark.django_db
class TestGamesCategories:
    """
    Tests API endpoints GET /api/games/ using query parameters to filter by
    genre, platform, developer, and publisher.
    """

    @pytest.mark.parametrize("category, value", [("genre", "action"),
                                                 ("platform", "pc"),
                                                 ("developer", "ea games"),
                                                 ("publisher", "nintendo"),
                                                 ("page", "5"),
                                                 ("idonotexist", "meeither")])
    def test_category(self, category, value):
        """
        Tests the 4 API endpoints with the structure
        GET /api/games/?category=value. Values must be case-insensitive.

        Passes when:
        - They each return a HTTP 200 OK.
        - Non-existent category returns a HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/games/?{category}={value}')
        
        # Check that every category is listing all its relevant data
        response = 200
        if category == "idonotexist": response = 404
        
        assert r.status_code == response

def test_method_not_allowed():
    """
    Tests POST /api/games/

    Passes when it returns a HTTP 405 Method Not Allowed.
    """
    # Need to authenticate here
    r = requests.post(f'{SERVER}api/games/')
    assert r.status_code == 405, f"Expected 405. Response = {r.status_code}."
