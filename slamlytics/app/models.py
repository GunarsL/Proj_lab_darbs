from . import db
from flask_login import UserMixin
from . import login_manager
from app import db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String, unique=True, nullable=False)
    home_team = db.Column(db.String(50))
    visitor_team = db.Column(db.String(50))
    home_score = db.Column(db.Integer)
    visitor_score = db.Column(db.Integer)
    date = db.Column(db.Date)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    home_team = db.Column(db.String(50), nullable=False)
    visitor_team = db.Column(db.String(50), nullable=False)

    lr_prob_team1_win = db.Column(db.Float)
    rf_prob_team1_win = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship("User", backref="predictions")

