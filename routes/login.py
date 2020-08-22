import os
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, login_user

from modules.db.User import User
# Blueprint Configuration
from routes.forms import LoginForm
from startFlask import login_manager, db

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@auth_bp.route("/logout")
@login_required
def logout_page():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login_page'))


@login_manager.user_loader
def load_user(user_mail):
    """Vérifie si l'utilisateur est loggué à chaque chargement de page"""
    if user_mail is not None:
        user = db.session.query(User).filter(User.email == user_mail).first()
        return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('Vous devez être identifié pour acceder à cette page.')
    return redirect(url_for('auth_bp.login_page'))


@auth_bp.route('/login', methods=['POST', 'GET'])
def login_page():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or user.password != password:
        flash('Vérifier vos information de connexion, puis essayez à nouveau.')
        return render_template('login.html', form=LoginForm())

    login_user(user)
    return redirect(url_for('home'))
