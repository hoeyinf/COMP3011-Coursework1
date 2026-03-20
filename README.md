# COMP3011-Coursework1
Videogame Review REST API.
Live deployment at: https://hoeyinfoong.pythonanywhere.com/

This project provides an API service for users to create, read, update, and
delete reviews for videogames. There are also endpoints for retrieving user,
game, and review data.

Some of these endpoints also provide light data analysis.
For example, user profiles will calculate the user's average score,
rating distribution, favorite game genres, and favorite games.

All endpoints are documented in APIDocumentation.pdf. See section API Endpoints
for more detail.

## Installation
Requires Python 3.12.
1. Download repository and extract.
2. Create a new virtual environment: `python -m venv /path/to/new/virtual/environment`
3. Activate the environment: `/path/to/new/virtual/environment/bin/activate`
4. In the root repository folder, run the command  `pip install -r requirements.txt`
5. From the root folder, navigate to api_project/ then run `python manage.py runserver`
6. If successful, the terminal should display which local port the app is running on
e.g. http://127.0.0.1:8000/ and the API endpoints should be ready to use.

## API Endpoints
API Documentation is in APIDocumentation.pdf

The format for each endpoint is server + "api" + endpoint.
For example, with server = http://127.0.0.1:8000/ and endpoint = `/games/`,
the actual GET endpoint is http://127.0.0.1:8000/api/games/
For live deployment it would be: https://hoeyinfoong.pythonanywhere.com/api/games/



