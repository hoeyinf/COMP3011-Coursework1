# COMP3011-Coursework1
Videogame Review REST API.
Live deployment server at: https://hoeyinfoong.pythonanywhere.com/<br>
Example of a live GET API endpoint at: https://hoeyinfoong.pythonanywhere.com/api/games/

This project provides an API service for users to create, read, update, and
delete reviews for videogames. There are also endpoints for user creation,
and for retrieving user, game, and review data.

Some of these endpoints also provide light data analysis.
For example, user profiles will calculate the user's average score,
rating distribution, favorite game genres, and favorite games.

All endpoints are documented in APIDocumentation.pdf.

## Installation
Requires Python 3.12.
1. Download repository and extract.
2. Create a new virtual environment: `python -m venv /path/to/new/virtual/environment`
3. Activate the environment: `/path/to/new/virtual/environment/bin/activate`
4. In the root repository folder, run the command  `pip install -r requirements.txt`
5. From the root folder, navigate to api_project/ then run `python manage.py runserver`
6. If successful, the terminal should display which local port the app is running on
e.g. http://127.0.0.1:8000/. The API endpoints should be ready to use.

## API Endpoints
API Documentation is in APIDocumentation.pdf

The format for each endpoint is server + "api" + endpoint.
For example, with server = http://127.0.0.1:8000/ and endpoint = `/games/`,<br>
the actual GET endpoint is http://127.0.0.1:8000/api/games/<br>
instead of http://127.0.0.1:8000/games/
For live deployment it would be: https://hoeyinfoong.pythonanywhere.com/api/games/

## Testing
There are pytest unit tests available to check if the APIs are running correctly.
1. In api_project/tests/conftest.py, change the `SERVER` constant on line 6 to be your development server. If the server is http://127.0.0.1:8000/, this step is unnecessary.
2. While the server is running, open a new terminal and use `pytest` in the same folder that the server was run from.<br>
The terminal should then show the tests running and their results.




