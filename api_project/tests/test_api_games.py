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
    Tests API endpoints:
    - GET /api/games
    - GET /api/games/<game_id>
    - GET /api/games/<game_id>/analytics
    - GET /api/games/<game_id>/reviews
    """

    def test_get(self):
        """
        Tests GET /api/games.

        Passes when it returns the correct data and a HTTP 200 OK.
        """
        r = requests.get(f'{SERVER}api/games')
        games = Game.objects.all().order_by('-release_date')[:10]
        # Compare the results
        correct = []
        for i in range(10):
            correct.append(r.json()[i]['title'] == games[i].title and
                           r.json()[i]['rating'] == games[i].rating and
                           r.json()[i]['genre'] == games[i].genre and
                           r.json()[i]['title'] == games[i].title and
                           r.json()[i]['release_date'] == str(games[i].release_date) and
                           r.json()[i]['description'] == games[i].description)
            
        assert all(correct) and r.status_code == 200

    @pytest.mark.parametrize("game_id, response", [(VALID_GAME_ID, 200),
                                                   (INVALID_GAME_ID, 404)])
    def test_get_id_correct_http(self, game_id, response):
        """
        Tests GET /api/games/<game_id> for valid and invalid game_id for correct
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
        Tests GET /api/games/<game_id> on a valid game_id.

        Passes when it returns the correct data.
        """
        r = requests.get(f'{SERVER}api/games/{VALID_GAME_ID}')
        game = Game.objects.get(pk=VALID_GAME_ID)
        reviews = Review.objects.filter(game=VALID_GAME_ID).count()
        assert (r.json()['title'] == game.title and
                len(r.json()['reviews']) == reviews)
        
    def test_get_id_authenticated(self):
        """
        Tests GET /api/games/<game_id> for an authenticated user.

        Passes when it the response contains a link to post a review of the game.
        """
        r = requests.get(f'{SERVER}api/games/{VALID_GAME_ID}')
        assert 'post_review' in r.json()

    @pytest.mark.parametrize("game_id, response", [(VALID_GAME_ID, 200),
                                                   (INVALID_GAME_ID, 404)])
    def test_get_id_analytics_correct_http(self, game_id, response):
        """
        Tests GET /api/games/<game_id>/analytics for valid and invalid game_id
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
        Tests GET /api/games/<game_id>/reviews for a valid and invalid game_id.
        
        Passes when:
        - Valid game_id returns correct reviews and a HTTP 200 OK.
        - Invalid game_id returns a HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/games/{game_id}/reviews')
        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    def test_get_reviews_correct_data(self):
        """
        Tests GET /api/games/<game_id>/reviews for a valid game_id.
        
        Passes when the correct data is returned.
        """
        r = requests.get(f'{SERVER}api/games/{VALID_GAME_ID}/reviews')
        reviews = Review.objects.filter(game=VALID_GAME_ID)
        # Compares each review's data to see if it matches
        correct = []
        for i, review in enumerate(reviews):
            correct.append(r.json()['user']['username'] == review.user.username and
                           r.json()['game']['title'] == review.game.title and
                           r.json()['date'] == str(review.date) and
                           r.json()['score'] == review.score)
            
        assert all(correct)


@pytest.mark.django_db
class TestGamesCategories:
    """
    Tests API endpoints for different game categories:
    - GET /api/games/genres
    - GET /api/games/genres/<genre_id>
    - GET /api/games/platforms
    - GET /api/games/platforms/<platform_id>
    - GET /api/games/developers
    - GET /api/games/developers/<developer_id>
    - GET /api/games/publishers
    - GET /api/games/publishers/<publisher_id>
    """

    @pytest.mark.parametrize("category, model", [("genres", Genre),
                                                 ("platforms", Platform),
                                                 ("developers", Developer),
                                                 ("publishers", Publisher),
                                                 ("idonotexist", "")])
    def test_category(self, category, model):
        """
        Tests the 4 API endpoints with the structure GET /api/games/<category>.

        Passes when:
        - They each return the correct data and a HTTP 200 OK.
        - Non-existent category returns a HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/games/{category}')
        
        # Check that every category is listing all its relevant data
        response = 200
        correct = True
        if category == "idonotexist": response = 404
        else:
            categories = model.objects.all()
            for i, cat in enumerate(categories):
                if r.json()[i] != cat.name:
                    correct = False
                    break
        
        assert correct and r.status_code == response, (f"Expected = {response}. "
                                                       f"Response = {r.status_code}.")

    @pytest.mark.parametrize("category, model", [("genres", Genre),
                                                 ("platforms", Platform),
                                                 ("developers", Developer),
                                                 ("publishers", Publisher)])
    def test_category_id_valid(self, category, model):
        """
        Tests the 4 API endpoints with the structure
        GET /api/games/<category>/<category_id>, for all valid category_ids.

        Passes when they each return the correct data and a HTTP 200 OK.
        """
        categories = model.objects.all()
        correct = True
        response = True
        # Loops through each subcategory and checks that they match
        for cat in categories:
            r = requests.get(f'{SERVER}api/games/{category}/{cat.pk}')
            if r.status_code != 200:
                response = False
                break
            if r.json()['name'] != cat.name:
                correct = False
                break
            
        assert correct and response, (f"Response = {response}. "
                                      f"Data = {correct}.")

    @pytest.mark.parametrize("category", ["genres", "platforms", "developers",
                                          "publishers"])
    def test_category_id_invalid(self, category):
        """
        Tests the 4 API endpoints with the structure
        GET /api/games/<category>/<category_id>, with invalid category_ids.

        Passes when they each return a HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/games/{category}/-1')
        assert r.status_code == 404, f"Expected 404. Response = {r.status_code}."

def test_method_not_allowed():
    """
    Tests PUT /api/games/1.

    Passes when it returns a HTTP 405 Method Not Allowed.
    """
    r = requests.put(f'{SERVER}api/games/1')
    assert r.status_code == 405, f"Expected 405. Response = {r.status_code}."
