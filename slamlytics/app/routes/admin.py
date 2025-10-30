import re
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import current_user, login_required
from ..models import User, db
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__, url_prefix='/admin')

def is_strong_password(password):
    """
    Checks if password contains:
    - min 8 characters
    - at least 1 uppercase letter
    - at least 1 lowercase letter
    - at least 1 number
    - at least 1 special symbol
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
    return re.match(pattern, password) is not None

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You don't have admin permissions")
            return redirect(url_for("main.profile"))
        return func(*args, **kwargs)
    return wrapper


# ===============================
# ADMIN DASHBOARD
# ===============================
@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


# ===============================
# EDIT USER
# ===============================
@admin.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('password')
        is_admin = True if request.form.get('is_admin') == 'on' else False

        if new_username:
            user.username = new_username

        if new_password:
            if not is_strong_password(new_password):
                flash("Password must contain at least one lowercase, one uppercase, one number, one special character, and be at least 8 characters long.")
                return redirect(url_for('admin.edit_user', user_id=user.id))
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

        user.is_admin = is_admin
        db.session.commit()

        flash('User updated successfully')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin_edit_user.html', user=user)


# ===============================
# DELETE USER
# ===============================
@admin.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} deleted successfully')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin_confirm_delete.html', user=user)


# ===============================
# TOGGLE ADMIN PERMISSIONS
# ===============================
@admin.route('/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You can't change your own permission!")
        return redirect(url_for('admin.dashboard'))

    user.is_admin = not user.is_admin
    db.session.commit()

    status = "admin" if user.is_admin else "regular user"
    flash(f"User {user.username} now is {status}")
    return redirect(url_for('admin.dashboard'))


# ===============================
# CREATE USER
# ===============================
@admin.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = True if request.form.get('is_admin') == 'on' else False

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('admin.create_user'))

        if not is_strong_password(password):
            flash("Password must contain at least one lowercase, one uppercase, one number, one special character, and be at least 8 characters long.")
            return redirect(url_for('admin.create_user'))

        new_user = User(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            is_admin=is_admin
        )
        db.session.add(new_user)
        db.session.commit()

        flash(f'User {username} created successfully!')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin_create_user.html')
