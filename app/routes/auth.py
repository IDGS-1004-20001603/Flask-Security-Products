from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models.Models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security.utils import login_user, logout_user
from flask_security import login_required
from .. import userDataStore

auth = Blueprint('auth', __name__, url_prefix='/security')


@auth.route('login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        return render_template('/security/login.html')

    if (request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()

        if (not user or not check_password_hash(user.password, password)):
            flash("The user and/or password aren't corrects")
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == 'GET'):
        return render_template('/security/register.html')

    if (request.method == 'POST'):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email is in use')
            return redirect(url_for('auth.register'))

        userDataStore.create_user(username=username, email=email, password=generate_password_hash(password, method='sha256'))
        db.session.commit()
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
