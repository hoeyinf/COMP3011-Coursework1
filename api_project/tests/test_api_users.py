"""Unit tests for API methods regarding users."""
import pytest
import requests

INVALID_ID = 0

class TestUsers:
    """
    Tests authentication via Django's provided User model, as well as the
    following API endpoints:
    - GET /api/users/<user_id>
    - GET /api/users/<user_id>/reviews/
    - POST /api/users/
    """
    @pytest.fixture(autouse=True)
    def set_fixtures(self, server, valid_password, existing_review,
                     existing_user):
        """Sets fixures so that they can be called using self."""
        self.server = server
        self.valid_password = valid_password
        self.existing_user = existing_user
        self.existing_review = existing_review

    @pytest.mark.parametrize("username, password, response", [
        ("admin", "valid_password", 200),
        ("idonotexist", "valid_password", 401),
        ("admin", "thisisnotmypassword", 401)
        ])
    def test_get_jwt(self, username, password, response):
        """
        Tests getting a jwt at POST /api/token/
        
        Passes when valid credentials retrieve an access and refresh token and a
        HTTP 200 OK, and an invalid login returns a HTTP 401 Unauthorized.
        """
        if password == "valid_password": password = self.valid_password

        credentials = {"username": username, "password": password}
        r = requests.post(f"{self.server}api/token/", data=credentials)

        # Checks that tokens are in response for a successful login
        if response == 200:
            assert "access" in r.json() and "refresh" in r.json()

        assert r.status_code == response
    
    @pytest.mark.parametrize("user_id, response", [("existing_user", 200),
                                                   (INVALID_ID, 404),
                                                   ("", 404)])
    def test_get(self, user_id, response):
        """
        Tests GET /api/users/<user_id>
        
        Passes when:
        - Valid user_id returns the correct data and a HTTP 200 OK.
        - Invalid user_id returns a HTTP 404 Not Found.
        - No user_id returns a HTTP 404 Not Found.
        """
        if user_id == "existing_user": user_id = self.existing_user["id"]

        r = requests.get(f"{self.server}api/users/{user_id}")

        # Checks that user data matches fixture for a successful GET
        if response == 200:
            assert all(r.json()[key] == self.existing_user[key]
                       for key in self.existing_user)

        assert r.status_code == response

    @pytest.mark.parametrize("user_id, response", [("existing_user", 200),
                                                   (INVALID_ID, 404)])
    def test_get_reviews(self, user_id, response):
        """
        Tests GET /api/users/<user_id>/reviews/ on a valid and invalid user_id
        for correct HTTP responses.
        
        Passes when:
        - Valid user_id returns a correct review and a HTTP 200 OK.
        - Invalid user_id returns a HTTP 404 Not Found.
        """
        if user_id == "existing_user": user_id = self.existing_user["id"]

        r = requests.get(f"{self.server}api/users/{user_id}/reviews/")

        # Checks that one of the reviews retrieved matches the fixture
        if response == 200:
            for review in r.json():
                if review["id"] == self.existing_review["id"]:
                    assert all(review[key] == self.existing_review[key]
                               for key in self.existing_review)
                break
        
        assert r.status_code == response

    def test_get_reviews_size(self):
        """
        Tests GET /api/users/<user_id>/reviews/ on an existing user
        
        Passes when correct number of reviews is returned.
        """
        r = requests.get(
            f"{self.server}api/users/{self.existing_user["id"]}/reviews/"
        )
        n = len(r.json())

        assert n == 4, (f"Expected = 4. Result = {n}")

    @pytest.mark.parametrize("username, password, message, response", [
        ("admin", "valid_password", "Username 'admin' already taken.", 409),
        ("valid_username", "shortpass", "invalid_password", 400),
        ("valid_username", "password123", "invalid_password", 400),
        ("valid_username", "102934857", "invalid_password", 400),
        ("", "thisisavalidpassword", "Username '' is too short.", 400),
        ("valid_username", "valid_password", "", 201)
        ])
    def test_post(self, username, password, message, response):
        """
        Tests POST /api/users/ on a invalid usernames and passwords,
        and a valid login.
        
        Passes when the correct error messages and HTTP status codes are returned.
        """
        if password == "valid_password": password = self.valid_password
        if message == "invalid_password":
            message = "Invalid password. Must be at least 12 characters long "\
                      "with letters."

        credentials = {"username": username, "password": password}
        r = requests.post(f"{self.server}api/users/", data=credentials)

        # Checks that response contains the correct data
        if response == 201:
            # Reminder to delete the created user between tests manually
            assert "username" in r.json(), "Username not in response. "\
                                           "Remember to delete valid_username "\
                                           f"if HTML: {r.status_code} == 409."
            assert r.json()["username"] == username and "url" in r.json()
   
        else:
            assert r.json()["message"] == message
        
        assert r.status_code == response

    @pytest.mark.parametrize("field", ["username", "password", "neither"])
    def test_post_missing_credentials(self, field):
        """
        Tests POST /api/users/ with no provided username or password.
        
        Passes when the correct HTTP status codes and error messages are
        returned.
        """
        # Omits fields for each test
        data = {}
        if field != "neither": data[field] = field
        r = requests.post(f"{self.server}api/users/", data=data)
        
        assert (r.status_code == 400 and
                r.json()["message"] == "Username/password not provided.")

    @pytest.mark.parametrize("field", ["username", "password", "extra"])
    def test_post_bad_syntax(self, field):
        """
        Tests POST /api/users/ with bad syntax.
        
        Passes when the correct HTTP status code and error message is
        returned.
        """
        # Sets data for misspelled fields or an extra field for each test
        data = {"username": "admin", "password": self.valid_password}
        if field == "username": data["user"] = data.pop(field)
        elif field == "password": data["pw"] = data.pop(field)
        else: data["extra"] = "Extra field for funsies."
        
        r = requests.post(f"{self.server}api/users/", data=data)
        
        assert (r.status_code == 400 and
                r.json()["message"] == "Provided data fields are incorrect.")
