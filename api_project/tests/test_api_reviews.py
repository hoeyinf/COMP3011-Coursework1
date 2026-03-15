"""Unit tests for API methods regarding reviews."""
import datetime
import pytest
import requests
from games.models import Review

VALID_USER_ID = 2
VALID_GAME_ID = 1
VALID_REVIEW_ID = 1
INVALID_GAME_ID = 0
INVALID_USER_ID = 0
INVALID_REVIEW_ID = 0
SERVER = "http://127.0.0.1:8000/"

@pytest.mark.django_db
class TestReviews:
    """
    Tests API endpoints for reviews:
    - GET /api/reviews/<review__id>
    - POST /api/reviews/
    - PUT /api/reviews/<review__id>
    - DELETE /api/reviews/<review__id>
    """

    @pytest.mark.parametrize("review_id, response", [(VALID_REVIEW_ID, 200),
                                                     (INVALID_REVIEW_ID, 404)])
    def test_get_id_correct_http(self, review_id, response):
        """
        Tests GET /api/reviews/<review__id> for a valid and invalid review_id
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
        Tests GET /api/reviews/<review__id> for an existing review.
        
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
        Tests GET /api/reviews/<review__id> for a user on their own review.

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
        Tests POST /api/reviews/ for authenticated users on valid and
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
           r = requests.post(f'{SERVER}api/reviews/')
        else:
            payload = {'game': game_id, 'date': datetime.date.today(),
                       'score': 75, 'content': 'Example review content!!!'}
            r = requests.post(f'{SERVER}api/reviews', params=payload)
        # Deletes any review created by the above POST request
        if Review.objects.all().count() == new_id:
           Review.objects.get(pk=new_id).delete()

        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    @pytest.mark.parametrize("review_id, authenticated",
                             [(VALID_REVIEW_ID, True), (VALID_REVIEW_ID, False),
                              (INVALID_REVIEW_ID, True)])
    def test_put(self, review_id, authenticated):
        """
        Tests PUT /api/reviews/<review__id> for valid and invalid review_ids on an
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
        Tests PUT /api/reviews/<review__id> for a user trying to update another
        user's review.

        Passes when it returns a HTTP 403 Forbidden.
        """
        assert False

    @pytest.mark.parametrize("review_id, own", [(VALID_REVIEW_ID, True),
                                                (INVALID_REVIEW_ID, True),
                                                (VALID_REVIEW_ID, False)])
    def test_delete(self, review_id, own):
        """
        Tests DELETE /api/reviews/<review__id> for a valid and invalid review_id, and
        on another user's review.

        Passes when:
        - Valid review_id is deleted and returns a HTTP 204 No Content.
        - Invalid review_id returns a HTTP 404 Not Found.
        - Another user's review returns a HTTP 403 Forbidden.
        """
        assert False

    def test_delete_unauthenticated(self):
        """
        Tests DELETE /api/reviews/<review__id> for an unauthenticated
        user.
        
        Passes when it returns a HTTP 401 Unauthorized.
        """
        assert False