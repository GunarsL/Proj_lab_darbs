import os
import pandas as pd
from datetime import datetime
from app.models import Game, db

# Попытка импортировать app или create_app
try:
    from app import app
except ImportError:
    from app import create_app
    app = create_app()

EXCEL_DIR = "GAMES_24_25"

TEAM_ABBR = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BKN",
    "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS",
}

def parse_date(date_str: str):
    """Парсинг даты из разных форматов"""
    date_str = str(date_str).strip()
    for fmt in ("%Y-%m-%d", "%a, %b %d, %Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Неизвестный формат даты: {date_str}")

def to_abbr(team_name: str) -> str:
    """Преобразует полное название в аббревиатуру"""
    team_name = str(team_name).strip()
    if team_name not in TEAM_ABBR:
        raise ValueError(f"Неизвестная команда: {team_name}")
    return TEAM_ABBR[team_name]

def import_games_from_excel():
    added = 0
    for file in os.listdir(EXCEL_DIR):
        if not file.endswith((".xls", ".xlsx")):
            continue
        filepath = os.path.join(EXCEL_DIR, file)

        try:
            # Пробуем открыть Excel
            try:
                df = pd.read_excel(filepath)
            except Exception:
                # Если это HTML под видом XLS
                df = pd.read_html(filepath)[0]

            # Оставляем только нужные колонки
            df = df[
                ["Date", "Visitor/Neutral", "PTS", "Home/Neutral", "PTS.1"]
            ].rename(
                columns={
                    "Visitor/Neutral": "Visitor",
                    "PTS": "VisitorPts",
                    "Home/Neutral": "Home",
                    "PTS.1": "HomePts",
                }
            )

            for _, row in df.iterrows():
                try:
                    game_date = parse_date(row["Date"])
                    home_team = to_abbr(row["Home"])
                    visitor_team = to_abbr(row["Visitor"])
                    home_score = int(row["HomePts"])
                    visitor_score = int(row["VisitorPts"])

                    # Проверка дубликатов по дате, командам и счёту
                    existing_game = Game.query.filter_by(
                        date=game_date,
                        home_team=home_team,
                        visitor_team=visitor_team,
                        home_score=home_score,
                        visitor_score=visitor_score
                    ).first()

                    if existing_game:
                        print(f"Пропускаю {visitor_team} @ {home_team} {visitor_score}-{home_score} ({game_date}) — уже есть в БД")
                        continue

                    # Генерация game_id для базы
                    game_id = f"{game_date}_{home_team}_{visitor_team}_{home_score}_{visitor_score}"

                    print(f"Добавляю игру {visitor_team} @ {home_team} {visitor_score}-{home_score} ({game_date})")

                    game = Game(
                        game_id=game_id,
                        home_team=home_team,
                        visitor_team=visitor_team,
                        home_score=home_score,
                        visitor_score=visitor_score,
                        date=game_date,
                    )
                    db.session.add(game)
                    added += 1
                except Exception as e:
                    print(f"Ошибка в строке {file}: {e}")

            db.session.commit()
            print(f"Файл {file} обработан.")
        except Exception as e:
            print(f"Не удалось обработать {file}: {e}")

    print(f"Импорт завершён. Всего добавлено {added} игр.")

if __name__ == "__main__":
    with app.app_context():
        import_games_from_excel()
