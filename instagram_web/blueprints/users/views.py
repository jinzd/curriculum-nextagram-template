from flask import Blueprint, render_template, flash, redirect, request, url_for
from werkzeug.security import generate_password_hash
from models.user import User
import re
users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():

    user_input = User(
        username=request.form.get('user_username'),
        email=request.form.get('user_email'),
        password=generate_password_hash(request.form.get('user_password')
                                        ))
    password_validate = re.match(
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})", user_input.password)

    if password_validate:
        if user_input.save():
            flash(
                f" Dear {user_input.username}, account has successfully created", 'success')
            return redirect(url_for('users.create'))
        else:
            return render_template('users/new.html',
                                   username=request.form.get('user_username'),
                                   email=request.form.get('user_email'),
                                   password=generate_password_hash(
                                       request.form.get('user_password')),
                                   errors=user_input.errors
                                   )
    else:
        flash("Your password must: be a minimum of 8 or more characters. include a minimum of three of the following mix of character types: uppercase, lowercase, numbers, non-alphanumeric symbols, for example not be identical to your NEXTAGRAM account name or email address")


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return render_template('users/new.html')
    # "USERS done"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
