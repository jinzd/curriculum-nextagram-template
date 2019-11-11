from flask import Blueprint, render_template, flash, redirect, request, url_for
from werkzeug.security import generate_password_hash
from models.user import User
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
        password=generate_password_hash(request.form.get('user_password'))
    )
    if user_input.save():
        flash("successfully created user")
        return redirect(url_for('users.create'))
    else:
        return render_template(url_for('users.new'),
                               username=request.form.get('user_username'),
                               email=request.form.get('user_email'),
                               password=generate_password_hash(
                                   request.form.get('user_password'))
                               )


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
