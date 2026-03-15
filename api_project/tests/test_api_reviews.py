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
        Tests POST /api/reviews/

        Passes when:
        - Valid game returns a 201 HTTP Created.
        - Invalid game returns a HTTP 422 Unprocessable Content.
        - Existing review returns a HTTP 409 Conflict.
        - Unauthenticated user returns a HTTP 401 Unauthorized.
        """
        new_id = Review.objects.all().count() + 1
        # Does not authenticate when testing for unauthenticated user
        if response == 401:
           r = requests.post(f'{SERVER}api/reviews/')
        else:
            payload = {'game': game_id, 'date': datetime.date.today(),
                       'score': 75, 'content': 'Example review content!!!'}
            r = requests.post(f'{SERVER}api/reviews', data=payload)
        # Deletes any review created by the above POST request
        if Review.objects.all().count() == new_id:
           Review.objects.get(pk=new_id).delete()

        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")
        
    def test_post_correct_data(self):
        """
        Tests POST /api/reviews/ for an authenticated user on a valid game.

        Passes when the review is successfully and correctly created.
        """
        # Get current user:
        # Use current user to get their review_n = Review.objects.filter().count()
        payload = {'game': 1, 'date': datetime.date.today(), 'score': 75,
                   'content': 'Example review content!!!'}
        r = requests.post(f'{SERVER}api/reviews/', data=payload)

        # new_review = Review.objects.filter().latest('date')
        # new_review_n = Review.objects.filter().count()
        # correct = new_review.game.id == 1 and new_review.score == 75 and new_review.date == datetime.date.today() and new_review.content == 'Example review content!!!'
        # new_review.delete()
        # assert (review_n + 1 == new_review_n and correct)
        assert False

    @pytest.mark.parametrize("review_id, expected",
                             [(VALID_REVIEW_ID, 200), (VALID_REVIEW_ID, 401),
                              (INVALID_REVIEW_ID, 404), (VALID_REVIEW_ID, 403)])
    def test_put(self, review_id, expected):
        """
        Tests PUT /api/reviews/<review__id>.

        Passes when:
        - Valid review_id and authenticated user updates the correct review and
        returns a HTTP 200 OK.
        - Unauthenticated user returns a HTTP 401 Unauthorized.
        - Invalid review_id returns a HTTP 404 Not Found.
        - Valid review_id from an authenticated user that is not its author
        returns a HTTP 403 Forbidden
        """
        # review = Review.objects.get(id)
        # old_score = review.score
        # old_content = review.content
        # payload_score = old_score - 1 if old_score > 0 else: payload_score = 100
        # payload_content = f'{old_content}!'
        # if expected == 200 or expected == 403:
        #     if expected == 200: login
        #     else: bad login
        # payload = {'score': payload_score, 'content': payload_content}
        # r = requests.put(f'{SERVER}api/reviews/{review_id}', data=payload)
        # new_review = Review.objects.get(id)
        # if expected == 200:
        #     assert (new_review.score == old_score - 1 or new_review.score == 100) and new_review.content = f'{old_content}!' and  r.status_code == expected
        # else: assert new_review.score == old_score and new_review.content == old_content and r.status_code == expected
        assert False


    @pytest.mark.parametrize("expected", [204, 404, 401, 403])
    def test_delete(self, expected):
        """
        Tests DELETE /api/reviews/<review__id>.

        Passes when:
        - Valid review_id is deleted and returns a HTTP 204 No Content.
        - Invalid review_id returns a HTTP 404 Not Found.
        - Unauthenticated user returns a HTTP 401 Unauthorized
        - Another user's review returns a HTTP 403 Forbidden.
        """
        # review_id = Review.objects.latest('id').id + 1
        # review = Review(game=VALID_REVIEW_ID, score=50, content="Example content")
        # review.save()
        # if expected == 200 or expected == 403:
        #     if expected == 200: login
        #     else: bad login
        # r = requests.delete(f'{SERVER}api/reviews/{review_id}')
        # try:
        #     new_review = Review.objects.get(review_id)
        #     assert new_review.score == 50 and new_review.content = "Example content" and r.status_code == expected
        # except Review.DoesNotExist:
        #     assert r.status_code == expected
        assert False