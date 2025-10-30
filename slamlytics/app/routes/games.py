from flask import Blueprint, render_template
import requests

games_bp = Blueprint('games', __name__, url_prefix='/games')

API_URL = "https://www.balldontlie.io/api/v1/games"

@games_bp.route('/')
def games_list():
    games_data = []

    try:
        params = {"per_page": 30, "page": 1}
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            games_data = data.get('data', [])
            print(f"DEBUG: Fetched {len(games_data)} games")
        else:
            print("Error: Status code", response.status_code)
    except Exception as e:
        print("Error fetching games:", e)

    return render_template('games.html', games=games_data)
