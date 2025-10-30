import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from app.models import Game

def _prepare_dataframe():
    games = Game.query.order_by(Game.date).all()
    if not games:
        return pd.DataFrame(), pd.Series(dtype=int), []

    rows = []
    for g in games:
        winner = 1 if g.home_score > g.visitor_score else 0
        rows.append({
            'date': g.date,
            'team1': g.home_team,
            'team2': g.visitor_team,
            'score1': g.home_score,
            'score2': g.visitor_score,
            'team1_win': winner
        })

    df = pd.DataFrame(rows)
    df = df.sort_values('date')
    df['margin'] = df['score1'] - df['score2']

    top_teams = pd.concat([df['team1'], df['team2']]).value_counts().nlargest(30).index
    df = df[df['team1'].isin(top_teams) & df['team2'].isin(top_teams)].copy()

    for team in top_teams:
        df[team] = ((df['team1'] == team) | (df['team2'] == team)).astype(int)

    y = df['team1_win']
    X = df[top_teams]

    return X, y, list(top_teams), df

import numpy as np

def train_models(return_models=False):
    X, y, teams, df = _prepare_dataframe()

    if isinstance(X, pd.DataFrame) and X.empty:
        return {'error': 'No data'}, None, None

    if len(y) < 50:
        return {'error': 'Not enough games to train (need at least ~50).'}, None, None

    df = df.sort_values('date')
    df['weight'] = 1.0
    max_weight = 2.0

    for team in teams:
        team_games_idx = df[(df['team1'] == team) | (df['team2'] == team)].index
        n = len(team_games_idx)
        if n > 0:
            exp_weights = np.exp(np.linspace(0, np.log(max_weight), n))
            df.loc[team_games_idx, 'weight'] = exp_weights

    sample_weights = df['weight'].values

    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
        X, y, sample_weights, test_size=0.2, random_state=42, stratify=y
    )

    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train, sample_weight=w_train)
    y_pred_lr = lr.predict(X_test)
    y_prob_lr = lr.predict_proba(X_test)[:, 1]

    rf = RandomForestClassifier(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train, sample_weight=w_train)
    y_pred_rf = rf.predict(X_test)
    y_prob_rf = rf.predict_proba(X_test)[:, 1]

    results = {
        'lr_accuracy': float(accuracy_score(y_test, y_pred_lr)),
        'lr_auc': float(roc_auc_score(y_test, y_prob_lr)),
        'rf_accuracy': float(accuracy_score(y_test, y_pred_rf)),
        'rf_auc': float(roc_auc_score(y_test, y_prob_rf)),
        'n_train': int(len(y_train)),
        'n_test': int(len(y_test))
    }

    try:
        coef = {}
        if X.shape[1] <= 1000:
            coef_vals = lr.coef_[0]
            coef_df = pd.Series(coef_vals, index=X.columns).abs().sort_values(ascending=False).head(10)
            coef = coef_df.to_dict()
        rf_importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False).head(10).to_dict()
        results['lr_top_features'] = {k: float(v) for k, v in coef.items()}
        results['rf_top_features'] = {k: float(v) for k, v in rf_importances.items()}
    except Exception:
        pass

    team_scores = {}
    for team in teams:
        team_games = df[(df['team1'] == team) | (df['team2'] == team)]
        wins = ((team_games['team1'] == team) & (team_games['team1_win'] == 1)).sum() + \
               ((team_games['team2'] == team) & (team_games['team1_win'] == 0)).sum()
        total = len(team_games)
        if total > 0:
            team_scores[team] = wins / total

    top3_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    results['top3_teams'] = [{'team': t, 'win_prob': float(w)} for t, w in top3_teams]

    if return_models:
        return results, lr, rf
    return results, None, None

def predict_match(team1_code, team2_code, lr_model=None, rf_model=None):
    X, y, teams, df = _prepare_dataframe()

    if isinstance(X, pd.DataFrame) and X.empty:
        return {'error': 'No data'}

    base = pd.DataFrame(columns=X.columns)
    base.loc[0] = 0

    if team1_code in base.columns:
        base.loc[0, team1_code] = 1
    if team2_code in base.columns:
        base.loc[0, team2_code] = 1

    probs = {}
    if lr_model is not None:
        try:
            probs['lr_prob_team1_win'] = float(lr_model.predict_proba(base)[0, 1])
        except Exception:
            probs['lr_prob_team1_win'] = None
    if rf_model is not None:
        try:
            probs['rf_prob_team1_win'] = float(rf_model.predict_proba(base)[0, 1])
        except Exception:
            probs['rf_prob_team1_win'] = None

    return probs
