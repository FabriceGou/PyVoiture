import os
from flask import redirect, render_template, flash, Blueprint, request, session, url_for
from flask_login import login_required, logout_user, login_user, current_user

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
    """Check if user is logged-in on every page load."""
    if user_mail is not None:
        user = db.session.query(User).filter(User.email == user_mail).first()
        return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login_page'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or user.password!=password:
        flash('Please check your login details and try again.')
        return render_template('login.html', form=LoginForm())

    login_user(user)

    return redirect(url_for('home'))



    return render_template('accueil.html',
                           title='Flask-Login Tutorial.',
                           current_user=current_user)

