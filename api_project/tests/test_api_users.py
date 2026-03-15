"""Unit tests for API methods regarding users."""
import pytest
import requests
from django.contrib.auth import authenticate
from games.models import User, Review

VALID_USER_ID = 2
VALID_GAME_ID = 1
INVALID_GAME_ID = 0
INVALID_USER_ID = 0
SERVER = "http://127.0.0.1:8000/"


@pytest.mark.django_db
class TestUsers:
    """
    Tests authentication via Django's provided User model, as well as the
    following API endpoints:
    - GET /api/users/<user_id>
    - GET /api/users/<user_id>/reviews/
    - POST /api/users/
    """
    @pytest.mark.parametrize("username, password, valid", [
        ("valid_username", "thisisavalidpassword", True),
        ("idonotexist", "thisisavalidpassword", False),
        ("valid_username", "thisisnotmypassword", False)])
    def test_authentication(self, username, password, valid):
        """
        Tests logging in.
        
        Passes when it returns a valid login works and an invalid one does not.
        """
        # Creates user when checking for a valid password
        if username == "valid_username":
            user = User.objects.create_user(username, "", "thisisavalidpassword")
            user.save()
        # Logs in with credentials
        login = authenticate(username=username, password=password)
        
        if username == "valid_username": user.delete()

        if valid: assert login is not None
        if not valid: assert login is None
    
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
        Tests GET /api/users/<user_id>/reviews/ on a valid and invalid user_id
        for correct HTTP responses.
        
        Passes when:
        - Valid user_id returns correct reviews and a HTTP 200 OK.
        - Invalid user_id returns a HTTP 404 Not Found.
        """
        r = requests.get(f'{SERVER}api/users/{user_id}/reviews/')
        assert r.status_code == response, (f"Expected = {response}. "
                                           f"Response = {r.status_code}.")

    @pytest.mark.parametrize("user_id, expected", [(VALID_USER_ID, 4),
                                                   (1, 0)])
    def test_get_reviews_size(self, user_id, expected):
        """
        Tests GET /api/users/<user_id>/reviews/ on a users with and without
        reviews.
        
        Passes when correct number of reviews is returned for each user.
        """
        r = requests.get(f'{SERVER}api/users/{user_id}/reviews/')
        assert len(r.json()) == expected, (f"Expected = {expected}. "
                                           f"Result = {len(r.json())}")
    
    def test_get_reviews_correct_data(self):
        """
        Tests GET /api/users/<user_id>/reviews/ on a valid user with
        multiple reviews.
        
        Passes when it returns correct review data for all reviews.
        """
        r = requests.get(f'{SERVER}api/users/{VALID_USER_ID}/reviews/')
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

    @pytest.mark.parametrize("username, password, expected", [
        ("valid_username", "thisisavalidpassword", 201),
        ("admin", "thisisavalidpassword", 409),
        ("valid_username", "password123", 400),
        ("valid_username", "102934857", 400),
        ("", "thisisavalidpassword", 400)])
    def test_post(self, username, password, expected):
        """
        Tests POST /api/users/ on a valid and some invalid usernames and
        passwords.
        """
        credentials = {'username': username, 'password': password}
        user_n = User.objects.all().count()
        r = requests.post(f'{SERVER}api/users/', data=credentials)
        new_user_n = User.objects.all().count()
        
        # Checks that user is actually created for valid credentials
        if expected == 201:
            new_user = User.objects.latest('id')
            new_username = new_user.username
            # Deletes created user
            new_user.delete()
            assert (user_n + 1 == new_user_n and
                    username == new_username  and
                    r.status_code == expected)
        else:
            assert (user_n == new_user_n and
                    r.status_code == expected)
