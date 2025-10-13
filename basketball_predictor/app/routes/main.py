from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Game
from import_games import import_last_30_games

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        # Если пользователь уже вошёл, перенаправляем на профиль
        return redirect(url_for('main.profile'))
    # Иначе показываем главную страницу или login
    return render_template('login.html')

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)

@main_bp.route('/games')
@login_required
def games():
    page = request.args.get('page', 1, type=int)  # номер страницы из URL
    per_page = 30  # сколько игр на странице
    
    pagination = Game.query.order_by(Game.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    last_games = pagination.items
    
    return render_template(
        "games.html",
        games=last_games,
        pagination=pagination
    )

@main_bp.route('/import-games')
@login_required
def import_games_route():
    import_last_30_games()
    return redirect(url_for('main.games'))

@main_bp.route('/model')
@login_required
def model():
    return render_template('model.html')

@main_bp.route('/my-predictions')
@login_required
def predictions():
    return render_template('predictions.html')

@main_bp.route('/charts')
@login_required
def charts():
    return render_template('charts.html')
