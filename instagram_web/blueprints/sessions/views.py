from flask import Blueprint, render_template, flash, redirect, request, url_for
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
