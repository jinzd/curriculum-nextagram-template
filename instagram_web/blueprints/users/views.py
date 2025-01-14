from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from models.user import User
import re
from instagram_web.util.helper import upload_file_to_s3

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new_account', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():

    user_password = request.form['user_password']
    password_validate = re.match(
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})", user_password)

    if password_validate:
        hashed_password = generate_password_hash(user_password)
        user_input = User(username=request.form.get(
            'user_username'), email=request.form.get('user_email'), password=hashed_password)
        if user_input.save():
            flash(
                f" Dear {user_input.username}, account has successfully created", 'success')
            return redirect(url_for('sessions.new'))
        else:
            return render_template('users/new.html',
                                   username=request.form.get(
                                       'user_username'),
                                   email=request.form.get('user_email'),
                                   password=generate_password_hash(
                                       request.form.get('user_password')),
                                   errors=user_input.errors
                                   )
    else:
        flash("Your password must: be a minimum of 8 or more characters. include a minimum of three of the following mix of character types: uppercase, lowercase, numbers, non-alphanumeric symbols, for example not be identical to your NEXTAGRAM account name or email address")
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    return render_template('users/new.html')
    # "USERS done"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)

    if not user:
        return redirect(url_for('sessions.new'))

    return render_template('users/edit.html', user=user, profile_picture=current_user.profile_image_url)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)
    if current_user == user:  # current_user method is from Flask-Login
        current_user.username = request.form["up_username"]
        current_user.email = request.form["up_email"]
        if current_user.save():
            flash("please change the contain before click submit")
            return redirect(url_for('users.edit', id=id))


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@users_blueprint.route('/upshit', methods=['POST'])
@login_required
def up_image():
    file = request.files["user_pro_pic"]
    print(file.filename)               # The actual name of the file
    print(file.content_type)
    print(file.content_length)
    print(file.mimetype)

    if file and allowed_file(file.filename):
        upload_file_to_s3(file)
        u_p = User.update(profile_picture=file.filename).where(
            current_user.id == User.id)
        # User.update({profile_picture: file})
        if u_p.execute():
            flash('thank bitch', "success")
            return redirect(url_for('users.edit', id=current_user.id))
    else:
        flash('wrong file', 'danger')
        return redirect(url_for('users.edit', id=current_user.id))
    return redirect(url_for('users.edit', id=current_user.id))
