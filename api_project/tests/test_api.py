"""
Unit tests for API methods in games.views.
"""
import datetime
import pytest
import requests
from games.views_api import *
from games.serializers import *

VALID_USER_ID = 2
VALID_GAME_ID = 1
VALID_REVIEW_ID = 1
INVALID_GAME_ID = 0
INVALID_USER_ID = 0
INVALID_REVIEW_ID = 0
SERVER = "http://127.0.0.1:8000/"


@pytest.mark.django_db
class TestUsers:
    """
    Tests authentication via Django's provided User model, as well as the
    following API endpoints:
    - GET /api/users/<user_id>
    - GET /api/users/<user_id>/reviews
    """

    def test_authentication_valid(self):
        """
        Tests logging in with a valid username and password.
        
        Passes when it returns a HTTP 200 OK.
        """
        # Login with valid credentials using fixture, check that it was successful (auth.get_user)
        assert False
    
    def test_authentication_invalid(self):
        """
        Tests logging in with an invalid username or password.
        
        Passes when it returns a HTTP 401 Unauthorized.
        """
        # Login with valid credentials using fixture, check that it was successful (auth.get_user)
        assert False
    
    @pytest.mark.parametrize("user_id, response", [(VALID_USER_ID, 200),
                                                   (INVALID_USER_ID, 404)])
    def test_get_correct_http(self, user_id, response):
        """
        Tests GET /api/users/<user_id> on a valid and invalid user_id for
        correct HTTP responses.
        
        Passes when:
        - Valid user_id returns a HTTP 200 OK.
        - Invalid user_id returns a HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/users/{user_id}')
        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    def test_get_correct_data(self):
        """
        TESTS GET /api/users/<user_id> on a valid user_id.
        
        Passes when it returns the correct data for the user, including a link
        to their reviews.
        """
        r = requests.get(f'{SERVER}api/users/{VALID_USER_ID}')
        user = User.objects.get(pk=VALID_USER_ID)
        assert r.json()['username'] == user.username and 'reviews' in r.json()

    @pytest.mark.parametrize("user_id, response", [(VALID_USER_ID, 200),
                                                   (INVALID_USER_ID, 404)])
    def test_get_reviews_correct_http(self, user_id, response):
        """
        Tests GET /api/users/<user_id>/reviews on a valid and invalid user_id
        for correct HTTP responses.
        
        Passes when:
        - Valid user_id returns correct reviews and a HTTP 200 OK.
        - Invalid user_id returns a HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/users/{user_id}/reviews')
        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    @pytest.mark.parametrize("user_id, expected", [(VALID_USER_ID, 4),
                                                   (1, 0)])
    def test_get_reviews_size(self, user_id, expected):
        """
        Tests GET /api/users/<user_id>/reviews on a users with and without
        reviews.
        
        Passes when correct number of reviews is returned for each user.
        """
        r = requests.get(f'{SERVER}api/users/{user_id}/reviews')
        assert len(r.json()) == expected, (f"Expected = {expected}. "
                                           f"Result = {len(r.json())}")
    
    def test_get_reviews_correct_data(self):
        """
        Tests GET /api/users/<user_id>/reviews on a valid user with
        multiple reviews.
        
        Passes when it returns correct review data for all reviews.
        """
        r = requests.get(f'{SERVER}api/users/{VALID_USER_ID}/reviews')
        reviews = Review.objects.filter(user=VALID_USER_ID)
        # Loop through each review and check that it returns correct data
        correct = []
        for i, review in enumerate(reviews):
            correct.append((r.json()[i]['user']['username'] == review.user.username and
                            r.json()[i]['game']['title'] == review.game.title and
                            r.json()[i]['date'] == str(review.date) and
                            r.json()[i]['score'] == review.score and
                            r.json()[i]['content'] == review.content and
                            'url' in r.json()[i]['game'] and
                            'url' in r.json()[i]['user']))
        assert all(correct)


@pytest.mark.django_db
class TestReviews:
    """
    Tests API endpoints for reviews:
    - GET /api/reviews/<review_id>
    - POST /api/reviews
    - PUT /api/reviews/<review_id>
    - DELETE /api/reviews/<review_id>
    """

    @pytest.mark.parametrize("review_id, response", [(VALID_REVIEW_ID, 200),
                                                     (INVALID_REVIEW_ID, 404)])
    def test_get_id_correct_http(self, review_id, response):
        """
        Tests GET /api/reviews/<review_id> for a valid and invalid review_id
        for correct HTTP status codes.
        
        Passes when:
        - Valid ID returns the correct review and a HTTP 200 OK.
        - Invalid ID returns a HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/reviews/{review_id}')
        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    def test_get_id_correct_data(self):
        """
        Tests GET /api/reviews/<review_id> for an existing review.
        
        Passes when it returns the correct data for the review.
        """
        r = requests.get(f'{SERVER}api/reviews/{VALID_REVIEW_ID}')
        review = Review.objects.get(pk=VALID_REVIEW_ID)
        assert (r.json()['user']['username'] == review.user.username and
                r.json()['game']['title'] == review.game.title and
                r.json()['date'] == str(review.date) and
                r.json()['score'] == review.score and
                r.json()['content'] == review.content and
                'url' in r.json()['game'] and
                'url' in r.json()['user'])
    
    def test_get_own_id(self):
        """
        Tests GET /api/reviews/<review_id> for a user on their own review.

        Passes when it also provides a link to edit the review and returns a
        HTTP 200 OK.
        """
        r = requests.get(f'{SERVER}api/reviews/{VALID_REVIEW_ID}')
        assert False

    @pytest.mark.parametrize("game_id, response", [(VALID_GAME_ID, 201),
                                                   (INVALID_GAME_ID, 422),
                                                   (VALID_GAME_ID, 409),
                                                   (VALID_GAME_ID, 401)])
    def test_post_correct_http(self, game_id, response):
        """
        Tests POST /api/reviews authenticated users on valid and
        invalid games, on an existing review, and an unauthenticated user.

        Passes when:
        - Valid game returns a 201 HTTP Created.
        - Invalid game returns a HTTP 422 Unprocessable Content.
        - Existing review returns a HTTP 409 Conflict.
        - Unauthenticated user returns a HTTP 401 Unauthorized.
        """
        new_id = Review.objects.all().count() + 1
        # Does not authenticate when testing for unauthenticared user
        if response == 401:
           r = requests.post(f'{SERVER}api/reviews')
        else:
            payload = {'game': game_id, 'date': datetime.date.today(),
                       'score': 75, 'content': 'Example review content!!!'}
            r = requests.post(f'{SERVER}api/reviews', params=payload)
        # Deletes any review created by the above POST request
        if Review.objects.all().count() == new_id:
           Review.objects.get(pk=new_id).delete()

        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    @pytest.mark.parametrize("review_id,authenticated",
                             [(VALID_REVIEW_ID, True), (VALID_REVIEW_ID, False),
                              (INVALID_REVIEW_ID, True)])
    def test_put(self, review_id, authenticated):
        """
        Tests PUT /api/reviews/<review_id> for valid and invalid review_ids on an
        authenticated and unauthenticated user.

        Passes when:
        - Valid review_id and authenticated user updates the correct review and
        returns a HTTP 200 OK.
        - Unauthenticated user returns a HTTP 401 Unauthorized.
        - Invalid review_id returns a HTTP 404 Not Found.
        """
        assert False

    def test_put_forbidden(self):
        """
        Tests PUT /api/reviews/<review_id> for a user trying to update another
        user's review.

        Passes when it returns a HTTP 403 Forbidden.
        """
        assert False

    @pytest.mark.parametrize("review_id, own", [(VALID_REVIEW_ID, True),
                                                (INVALID_REVIEW_ID, True),
                                                (VALID_REVIEW_ID, False)])
    def test_delete(self, review_id, own):
        """
        Tests DELETE /api/reviews/<review_id> for a valid and invalid review_id, and
        on another user's review.

        Passes when:
        - Valid review_id is deleted and returns a HTTP 200 OK.
        - Invalid review_id returns a HTTP 404 Not Found.
        - Another user's review returns a HTTP 403 Forbidden.
        """
        assert False

    def test_delete_unauthenticated(self):
        """
        Tests DELETE /api/reviews/<review_id> for an unauthenticated
        user.
        
        Passes when it returns a HTTP 401 Unauthorized.
        """
        assert False


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
