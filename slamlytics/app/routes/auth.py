import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..models import User, db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

def is_strong_password(password):
    """
    Checks if password contains:
    - min 8 characters
    - at least 1 upperscale letter
    - at least 1 lowerscale letter
    - at least 1 number
    - at least 1 special symbol
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
    return re.match(pattern, password) is not None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        if not is_strong_password(password):
            flash('Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character.')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=username, 
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
