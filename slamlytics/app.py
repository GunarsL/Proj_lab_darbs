from app import create_app
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Game, Prediction
from app import db
from import_games import import_last_30_games
from ml_models import train_models, predict_match

main_bp = Blueprint('main', __name__)
app = create_app()

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('login.html')

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)

@main_bp.route('/games')
@login_required
def games():
    page = request.args.get('page', 1, type=int)
    per_page = 30 
    
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
    results, lr_model, rf_model = train_models(return_models=True)

    try:
        import pickle
        with open('models/lr_model.pkl', 'wb') as f:
            pickle.dump(lr_model, f)
        with open('models/rf_model.pkl', 'wb') as f:
            pickle.dump(rf_model, f)
    except Exception:
        pass

    return render_template('model.html', lr_summary=results, rf_summary=results)

@main_bp.route('/my-predictions')
@login_required
def predictions():
    user_predictions = current_user.predictions
    return render_template('predictions.html', predictions=user_predictions)

@main_bp.route('/create-prediction', methods=['GET', 'POST'])
@login_required
def create_prediction():
    teams = {
        "ATL":"Atlanta Hawks","BOS":"Boston Celtics","BKN":"Brooklyn Nets",
        "CHA":"Charlotte Hornets","CHI":"Chicago Bulls","CLE":"Cleveland Cavaliers",
        "DAL":"Dallas Mavericks","DEN":"Denver Nuggets","DET":"Detroit Pistons",
        "GSW":"Golden State Warriors","HOU":"Houston Rockets","IND":"Indiana Pacers",
        "LAC":"Los Angeles Clippers","LAL":"Los Angeles Lakers","MEM":"Memphis Grizzlies",
        "MIA":"Miami Heat","MIL":"Milwaukee Bucks","MIN":"Minnesota Timberwolves",
        "NOP":"New Orleans Pelicans","NYK":"New York Knicks","OKC":"Oklahoma City Thunder",
        "ORL":"Orlando Magic","PHI":"Philadelphia 76ers","PHX":"Phoenix Suns",
        "POR":"Portland Trail Blazers","SAC":"Sacramento Kings","SAS":"San Antonio Spurs",
        "TOR":"Toronto Raptors","UTA":"Utah Jazz","WAS":"Washington Wizards"
    }

    if request.method == 'POST':
        home_team = request.form.get('home_team')
        visitor_team = request.form.get('visitor_team')

        if home_team == visitor_team:
            from flask import flash
            flash("Home team and visitor team cannot be the same!", "error")
            return render_template('create_prediction.html', teams=teams)

        results, lr_model, rf_model = train_models(return_models=True)

        probs = predict_match(home_team, visitor_team, lr_model, rf_model)

        new_prediction = Prediction(
            user_id=current_user.id,
            home_team=home_team,
            visitor_team=visitor_team,
            lr_prob_team1_win=probs.get('lr_prob_team1_win'),
            rf_prob_team1_win=probs.get('rf_prob_team1_win')
        )
        db.session.add(new_prediction)
        db.session.commit()

        return redirect(url_for('main.predictions'))

    return render_template('create_prediction.html', teams=teams)

@main_bp.route('/delete-prediction/<int:prediction_id>', methods=['POST'])
@login_required
def delete_prediction(prediction_id):
    pred = Prediction.query.get_or_404(prediction_id)
    if pred.user_id != current_user.id:
        return "Forbidden", 403
    db.session.delete(pred)
    db.session.commit()
    return redirect(url_for('main.predictions'))


@main_bp.route('/charts')
@login_required
def charts():

    predictions = Prediction.query.all()
    games = Game.query.all()

    metrics = {
        "lr": {"TP": 0, "FP": 0},
        "rf": {"TP": 0, "FP": 0},
    }

    scores = {"lr": 0, "rf": 0}

    for pred in predictions:
        game = next(
            (g for g in games
             if g.home_team == pred.home_team
             and g.visitor_team == pred.visitor_team
             and pred.created_at.date() <= g.date),
            None
        )
        if not game:
            continue

        true_winner = game.home_team if game.home_score > game.visitor_score else game.visitor_team

        if pred.lr_prob_team1_win is not None:
            lr_pred_winner = pred.home_team if pred.lr_prob_team1_win >= 0.5 else pred.visitor_team
            if lr_pred_winner == true_winner:
                metrics["lr"]["TP"] += 1
            else:
                metrics["lr"]["FP"] += 1


        if pred.rf_prob_team1_win is not None:
            rf_pred_winner = pred.home_team if pred.rf_prob_team1_win >= 0.5 else pred.visitor_team
            if rf_pred_winner == true_winner:
                metrics["rf"]["TP"] += 1
            else:
                metrics["rf"]["FP"] += 1

        if pred.lr_prob_team1_win is not None and pred.rf_prob_team1_win is not None:
            lr_pred = pred.home_team if pred.lr_prob_team1_win >= 0.5 else pred.visitor_team
            rf_pred = pred.home_team if pred.rf_prob_team1_win >= 0.5 else pred.visitor_team

            if lr_pred == true_winner and rf_pred == true_winner:
                if pred.lr_prob_team1_win > pred.rf_prob_team1_win:
                    scores["lr"] += 1
                else:
                    scores["rf"] += 1
            elif lr_pred == true_winner:
                scores["lr"] += 1
            elif rf_pred == true_winner:
                scores["rf"] += 1
            else:
                if abs(pred.lr_prob_team1_win - 0.5) < abs(pred.rf_prob_team1_win - 0.5):
                    scores["lr"] += 1
                else:
                    scores["rf"] += 1

    return render_template("charts.html", results=metrics, scores=scores)



if __name__ == "__main__":
    app.run(debug=True)
