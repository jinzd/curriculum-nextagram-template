from flask import Blueprint, render_template, flash, redirect, request, url_for
from instagram_web.helpers.google_oauth import oauth
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from flask_login import current_user, login_user, logout_user, login_required
import re
sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])  # done
# @login_required
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])  # done
def create():

    user = User.get_or_none(
        User.email == request.form['signin_email'])
    if user:

        password_is_correct = check_password_hash(
            user.password, request.form['signin_password'])
        if password_is_correct:
            login_user(user)
            print(current_user.username)
            flash(f"Welcome {current_user.username}", "success")
            return redirect(url_for('home'))
        else:
            flash("incorrect password", "danger")
            return redirect(url_for('sessions.new'))
    else:
        flash("no such user", "danger")
        return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/login/google', methods=["GET"])
def google_login():
    redirect_uri = url_for('sessions.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/authorize/google', methods=["GET"])
def authorize_google():
    token = oauth.google.authorize_access_token()
    if not token:
        flash('Oops, some shit din happen', 'danger')
        return redirect(url_for('home'))

    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']

    user = User.get_or_none(User.email == email)
    if not user:
        flash('Sorry, no account registern', 'danger')
        return redirect(url_for('home'))
    login_user(user)
    flash(f'Welcome {current_user.username}', 'success')
    return redirect(url_for('home'))


@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@sessions_blueprint.route('/', methods=["GET"])
@login_required
def index():
    # pass
    return render_template('sessions/new.html')
    # "sessions done"


@sessions_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass
    #     user = User.get_by_id(id)

    # if current_user == user:


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass


@sessions_blueprint.route("/destroy", methods=['GET'])  # done
@login_required
def destroy():
    logout_user()
    flash("Signed Out", "danger")
    return redirect(url_for('sessions.new'))
