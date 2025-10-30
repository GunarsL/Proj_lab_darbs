import os
import requests
from app.models import Game, db
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.balldontlie.io/v1/games"
API_KEY = os.getenv("BALLDONTLIE_API_KEY")
print("API_KEY:", API_KEY)

def import_last_30_games():
    try:
        print("Importing last 30 games")

        today = datetime.today().date()
        three_months_ago = today - timedelta(days=150)

        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(
            API_URL,
            params={
                "start_date": three_months_ago.strftime("%Y-%m-%d"),
                "end_date": today.strftime("%Y-%m-%d"),
                "per_page": 100,
            },
            headers=headers
        )
        response.raise_for_status()
        data = response.json().get("data", [])

        data.sort(key=lambda g: g["date"], reverse=True)

        added = 0
        for row in data:
            if row.get("status") != "Final":
                continue

            game_id = str(row.get("id"))
            date_str = row.get("date", "")[:10]
            game_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            home_team = row["home_team"]["abbreviation"]
            visitor_team = row["visitor_team"]["abbreviation"]
            home_score = row.get("home_team_score", 0)
            visitor_score = row.get("visitor_team_score", 0)

            exists = Game.query.filter_by(game_id=game_id).first()
            if exists:
                continue

            game = Game(
                game_id=game_id,
                home_team=home_team,
                visitor_team=visitor_team,
                home_score=int(home_score),
                visitor_score=int(visitor_score),
                date=game_date
            )
            db.session.add(game)
            added += 1

        db.session.commit()
        print(f"Import is complete, added new {added} games.")

    except Exception as e:
        print("Error getting data:", e)
