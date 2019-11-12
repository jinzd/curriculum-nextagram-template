from flask import Blueprint, render_template, flash, redirect, request, url_for
from werkzeug.security import generate_password_hash
from models.user import User
import re
users_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@users_blueprint.route('/', methods=['POST'])
def login():
    user_input = User(
        email=request.form.get('input_email'),
        password=generate_password_hash(request.form.get('input_password')
                                        ))
    return render_template('sessions/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    pass
    # return render_template('sessions/new.html')
    # "USERS done"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
