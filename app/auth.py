from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db
from app.forms import LoginForm, RegisterForm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form, disable_player=True)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Create a new user with hashed password
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, disable_player=True)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
