"""Unit tests for API methods regarding reviews."""
import datetime
import pytest
import requests

INVALID_ID = 0

class TestReviews:
    """
    Tests API endpoints for reviews:
    - GET /api/reviews/<review__id>
    - POST /api/reviews/
    - PATCH /api/reviews/<review__id>
    - DELETE /api/reviews/<review__id>
    """

    @pytest.fixture(autouse=True)
    def set_fixtures(self, server, new_review, patch_review, existing_review):
        """Sets fixures so that they can be called using self."""
        self.server = server
        self.new_review = new_review
        self.patch_review = patch_review
        self.existing_review = existing_review

    @pytest.mark.parametrize("review_id, response", [("existing_review", 200),
                                                     (INVALID_ID, 404),
                                                     ("", 404)])
    def test_get_id(self, review_id, response):
        """
        Tests GET /api/reviews/<review__id>

        Passes when:
        - Valid review_id returns the correct review and a HTTP 200 OK.
        - Invalid review_id returns a HTTP 404 Not Found.
        - No review_id returns a HTTP 404 Not Found.
        """
        if review_id == "existing_review": review_id = self.existing_review["id"]

        r = requests.get(f"{self.server}api/reviews/{review_id}")

        # Checks the data matches fixture for a successful GET
        if response == 200:
            assert all(r.json()[key] == self.existing_review[key]
                       for key in self.existing_review)

        assert r.status_code == response

    @pytest.mark.parametrize("message, response", [
        ("Provided fields are incorrect.", 400),
        ("Required fields not provided.", 400),
        ("Not authenticated (jwt not found).", 401),
        ("Review already exists.", 409),
        ("Game with id=0 not found.", 404)])
    def test_post_invalid_request(self, message, response, admin_jwt):
        """
        Tests POST /api/reviews/ for an unauthenticated user,
        an already existing review, and bad syntax in request data.

        Passes when:
        - Bad request syntax returns a HTTP 400 Bad Request
        - Unauthenticated user returns a HTTP 401 Unauthorized.
        - Existing review returns a HTTP 409 Conflict.
        - Invalid game returns a HTTP 404 Not Found
        """
        # Sets data based on test conditions
        data = self.new_review
        if response == 400:
            if message == "Required fields not provided.":
                data.pop("score")
            else:
                data["game_id"] = data.pop("game")
        elif response == 404: data["game"] = INVALID_ID
        elif response == 409:
            data = self.patch_review
            data.pop("id")
            data["game"] = 495
            data["date"] = datetime.date.today().strftime("%Y-%m-%d")

        # Does not authenticate for unauthenticated test
        if response == 401:
            r = requests.post(f"{self.server}api/reviews/", data=data)
        else:
            r = requests.post(f"{self.server}api/reviews/",
                              headers={"Authorization": f"Bearer {admin_jwt}"},
                              data=data)

        assert r.status_code == response and r.json()["message"] == message

    @pytest.mark.parametrize("field, value",[
        ("date", (datetime.date.today()+datetime.timedelta(days=1))),
        ("date", "January 1 2030"), ("score", -1), ("score", 101),
        ("score", "five stars")])
    def test_post_invalid_values(self, field, value, admin_jwt):
        """
        Tests POST /api/reviews/ for invalid values in request.

        Passes when they all return a HTTP 400 Bad Request.
        """
        # Sets data based on test conditions
        data = self.new_review
        data[field] = value

        r = requests.post(f"{self.server}api/reviews/",
                            headers={"Authorization": f"Bearer {admin_jwt}"},
                            data=data)

        assert r.status_code == 400, (f"If {r.status_code} == 201, you need to"\
                                     " manually delete the post from database.")
        assert field in r.text

    def test_post_valid(self, admin_jwt):
        """
        Test that POST /api/reviews/ works.

        Passes when it returns the correct data and a HTTP 201 Created.
        """
        # Check that GET user reviews is working before testing post
        admin = requests.get(f"{self.server}api/users/1/reviews/")
        assert admin.status_code == 200, ("Can not test if GET api endpoints "\
                                          "are not working properly.")

        r = requests.post(f"{self.server}api/reviews/",
                            headers={"Authorization": f"Bearer {admin_jwt}"},
                            data=self.new_review)

        # Reminders to manually delete entries in database if needed
        admin = requests.get(f"{self.server}api/users/1/reviews")
        assert len(admin.json()) == 2, ("Wrong review length. Manually "\
                                        "check admin reviews and fix.")

        # Checks that the new review is correct
        for review in admin.json():
            if review["content"] == self.new_review["content"]:
                break
        assert ("id" in review and "url" in review and
                review["user"]["username"] == "admin" and
                review["game"]["url"] == f"{self.server}api/games/"\
                                         f"{self.new_review['game']}" and
                review["date"] == self.new_review["date"] and
                review["score"] == self.new_review["score"] and
                review["content"] == self.new_review["content"] and
                r.status_code == 201)

        # Delete new review if needed
        delete = requests.delete(f"{self.server}api/reviews/{review["id"]}",
                                    headers={"Authorization": f"Bearer {admin_jwt}"})
        assert delete.status_code == 204, ("Delete failed. Please manually "\
                                           "delete new review if needed.")

    @pytest.mark.parametrize("message, response", [
        ("Provided fields are incorrect.", 400),
        ("Review not provided.", 400),
        ("Need to provide score or content to update.", 400),
        ("Not authenticated (jwt not found).", 401),
        ("You are not the author.", 403),
        ("Review with id=0 not found.", 404)])
    def test_patch_invalid_request(self, message, response, admin_jwt, valid_password):
        """
        Tests PATCH /api/reviews/<review__id> for an unauthenticated user,
        a non-existent review, on another user's review, and bad syntax in
        request data.

        Passes when:
        - Bad syntax returns a HTTP 400 Bad Request.
        - Unauthenticated user returns a HTTP 401 Unauthorized.
        - Valid review from an authenticated user that is not its author
        returns a HTTP 403 Forbidden.
        - Invalid review returns a HTTP 404 Not Found.
        """
        # Sets data to be different than fixture
        data = self.patch_review
        id = data.pop("id")
        data["score"] = 42
        data["content"] = "Review updated successfully"

        # Sets data based on and test conditions
        if response == 400:
            if message == "Provided fields are incorrect.":
                data["rating"] = data.pop("score")
            elif message == "Review not provided.": id = ""
            else:
                data.pop("score")
                data.pop("content")
        elif response == 404: id = INVALID_ID
        # Logins in with different user
        if response == 403:
            login = requests.post(f"{self.server}api/token/",
                                  data={"username":"valid_username",
                                        "password": valid_password})
            jwt = login.json()["access"]
        else: jwt = admin_jwt

        if response == 401:
            r = requests.patch(f"{self.server}api/reviews/{id}",
                               data=data)
        else:
            r = requests.patch(f"{self.server}api/reviews/{id}",
                               headers={"Authorization": f"Bearer {jwt}"},
                               data=data)

        # If successful, assume that it works correctly to undo the update
        if r.status_code == 204:
            requests.patch(f"{self.server}api/reviews/{self.patch_review["id"]}",
                             headers={"Authorization": f"Bearer {jwt}"},
                             data=self.patch_review)
        
        assert r.status_code == response and r.json()["message"] == message

    @pytest.mark.parametrize("value", [-1, 101, "ten"])
    def test_patch_invalid_scores(self, value, admin_jwt):
        """
        Tests PATCH /api/reviews/<review__id> for invalid scores in request.

        Passes when they all return a HTTP 400 Bad Request and appropriate
        error message.
        """
        data = self.patch_review
        id = data.pop("id")
        data["score"] = value

        r = requests.patch(f"{self.server}api/reviews/{id}",
                           headers={"Authorization": f"Bearer {admin_jwt}"},
                           data=data)

        # If successful, assume that it works correctly to undo the update
        if r.status_code == 204:
            requests.patch(f"{self.server}api/reviews/{id}",
                           headers={"Authorization": f"Bearer {admin_jwt}"},
                           data=self.patch_review)
        
        assert r.status_code == 400 and "score" in r.text

    @pytest.mark.parametrize("new_data", [
        ({"score": 0, "content": "Updated successfully"}), ({"score": 0}),
        ({"content": "Updated successfully"})
        ])
    def test_patch_valid(self, new_data, admin_jwt):
        """
        Tests PATCH /api/reviews/<review__id> valid requests, making sure that
        excluding a field has intended behaviour.

        Passes when they all return a HTTP 200 OK.
        """
        # Sets data based on test conditions
        data = self.patch_review.copy()
        id = data.pop("id")
        for key in ["score", "content"]:
            if key in new_data: data[key] = new_data[key]
            else: data.pop(key)

        r = requests.patch(f"{self.server}api/reviews/{id}",
                           headers={"Authorization": f"Bearer {admin_jwt}"},
                           data=data)

        # Check that review is now updated
        check = requests.get(f"{self.server}api/reviews/{id}")
        assert check.status_code == 200, "Could not verify review status."
        review = check.json()
        assert (review["id"] == id and review["user"]["username"] == "admin" and
                review["game"]["title"] == "Disco Elysium: The Final Cut" and
                all(review[key] == data[key] for key in new_data))
        
        # If successful, assume that it works correctly to undo the update
        if r.status_code == 204:
            redata = self.patch_review
            redata.pop("id")
            repatch = requests.patch(f"{self.server}api/reviews/{id}",
                                     headers={"Authorization": f"Bearer {admin_jwt}"},
                                     data=redata)
            assert repatch.status_code == 204, "Repatch failed!"

        assert r.status_code == 204
        

    @pytest.mark.parametrize("message, response", [
        ("", 204),
        ("Review not provided.", 400),
        ("Review not found.", 404),
        ("Not authenticated (jwt not found).", 401),
        ("You are not the author.", 403)])
    def test_delete(self, message, response, admin_jwt, valid_password):
        """
        Tests DELETE /api/reviews/<review__id>.

        Passes when:
        - Valid review_id is deleted and returns a HTTP 204 No Content.
        - Invalid review_id returns a HTTP 404 Not Found.
        - Unauthenticated user returns a HTTP 401 Unauthorized
        - Another user's review returns a HTTP 403 Forbidden.
        """
        # Creates new post to test for deletion
        new_review = self.new_review
        new_review["game"] = 1234
        new_review["content"] = "Created to test deletion."
        post = requests.post(f"{self.server}api/reviews/",
                             headers={"Authorization": f"Bearer {admin_jwt}"},
                             data=new_review)
        assert post.status_code == 201, (f"{post.status_code} == 201"\
                                         "New review could not be created.")

        # Sets parameters based on test conditions
        if response == 400: review_id = ""
        else: review_id = post.json()["id"]
        jwt = admin_jwt
        if response == 404: review_id = INVALID_ID
        elif response == 403:
            login = requests.post(f"{self.server}api/token/",
                                  data={"username":"valid_username",
                                        "password": valid_password})
            jwt = login.json()["access"]

        if response == 401:
            r = requests.delete(f"{self.server}api/reviews/{review_id}")
        else:
            r = requests.delete(f"{self.server}api/reviews/{review_id}",
                                headers={"Authorization": f"Bearer {jwt}"},)

        assert r.status_code == response, (
            f"{r.status_code} == {response}. "\
            "Check database to delete this review if needed.")

        if response != 204:
            assert r.json()["message"] == message
            # Deletes any actual review that's still there
            admin_reviews = requests.get(f"{self.server}api/users/1/reviews/")
            for review in admin_reviews.json():
                if review["content"] == "Created to test deletion.":
                    requests.delete(review["url"],
                                    headers={"Authorization": f"Bearer {admin_jwt}"})
