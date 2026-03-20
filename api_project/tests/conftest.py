"""Defines fixtures used for testing."""
import datetime
import pytest
import requests

SERVER = "http://127.0.0.1:8001/"
PASSWORD = "nothtesameasdeployedpassword"

@pytest.fixture
def server():
    return SERVER

@pytest.fixture
def valid_password():
    return PASSWORD

@pytest.fixture
def admin_jwt():
    """Fixture to get jwt for the admin account."""
    login = requests.post(f'{SERVER}api/token/', data={"username":"admin",
                                                       "password": PASSWORD})
    return login.json()['access']

@pytest.fixture
def existing_user():
    """Fixture for a user (unknown password but existing data)."""
    return {"id": 2,
            "username": "Filipe69",
            "url": f"{SERVER}api/users/2",
            "reviews": f"{SERVER}api/users/2/reviews/"}

@pytest.fixture
def existing_review():
    """Fixture for an existing review (from existing_user)."""
    return {"id": 67956,
            "url": f"{SERVER}api/reviews/67956",
            "user": {"username": "Filipe69",
                     "url": f"{SERVER}api/users/2"},
            "game": {"title": "The Legend of Zelda Collector's Edition",
                     "url": f"{SERVER}api/games/39"},
            "date": "2023-03-05",
            "score": 100,
            "content": "Édition légendaire, réuni 2 grands chefs du jeu vidéo."\
                       " Cet édition a du mettre tout le monde d’accord. Avec "\
                       "cette petite démo de Wind Waker qui nous a fait rêver"}

@pytest.fixture
def existing_game():
    """Fixture for an existing game (same as the one in existing_review)."""
    return {"id": 39,
            "title": "The Legend of Zelda Collector's Edition",
            "url": f"{SERVER}api/games/39",
            "release_date": "2003-11-17",
            "rating": "E",
            "description": "The greatest legend in gaming! The ultimate Zelda "\
                           "collection!\n\n- The Legend of Zelda: Play the gam"\
                           "e that launched the legend! With an innovative and"\
                           " unique game-play system, remarkably deep puzzle s"\
                           "olving, and an epic score, the appeal of this grou"\
                           "ndbreaking classic is still going strong.\n\n- Zel"\
                           "da II - The Adventure of Link: While adhering to t"\
                           "he majestic and puzzle-solving elements of the Leg"\
                           "end of Zelda, the second game in the series expand"\
                           "s on the action sequences and introduces a new mag"\
                           "ic system, pushing the series in a new direction."\
                           "\n\n- The Legend of Zelda: Ocarina of Time: Zelda "\
                           "moved into three dimensions with gorgeous cinemati"\
                           "cs, hordes of hostile enemies, the revolutionary t"\
                           "argeting system, and the freedom of traveling on h"\
                           "orseback. Ocarina of Time leaves all who play it b"\
                           "reathless and impressed.\n\n- The Legend of Zelda:"\
                           " Majora's Mask: The series again takes a dramatic "\
                           "turn from tradition as Link wanders into a three-d"\
                           "ay journey in a mysterious parallel world. Majora'"\
                           "s Mask challenges players to don magical masks and"\
                           " save a town threatened to be crushed under a mena"\
                           "cing moon.\n\nIncludes Playable Demo for The Legen"\
                           "d of Zelda: The Wind Waker!",
            "genre": "Compilation",
            "platforms": ["GameCube"],
            "developers": ["Nintendo"],
            "publishers": ["Nintendo"],
            "reviews": f"{SERVER}api/games/39/reviews/",
            "analytics": f"{SERVER}api/games/39/analytics"}

@pytest.fixture
def new_review():
    """Fixture for creating a new review (admin reviewing existing_game)."""
    return {"game": 39,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "score": 88,
            "content": "This is a review created by testing."}

@pytest.fixture
def patch_review():
    """Fixture for existing admin review to test updating a review."""
    # Note: pop id to use for url. Only score and/or content needed to patch
    return {"id": 130001,
            "score": 100,
            "content": "Best game of all time."}
