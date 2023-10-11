from flask import Blueprint, render_template, request,flash,redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
      if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email = email).first()
            if user:
                  if check_password_hash(user.password, password):
                        flash('Logged in successfully', category='success')
                        login_user(user, remember=True)
                        return redirect(url_for('views.home'))
                  else:
                        flash('Incorrect password, try again', category='error')
            else:
                  flash('Email does not exist.', category='error')
                  

      return render_template('login.html',user = current_user)

@auth.route('/signUp', methods=['GET', 'POST'])
def signUp():
      if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            user = User.query.filter_by(email=email).first()

            if len(email)<11:
                  flash('Invalid Email', category='error')
            elif user:
                  flash('Email already exist', category='error')
            elif len(first_name)<2:
                  flash('Invalid firstName', category='error')
            elif len(password1)<2:
                  flash('password length is less than two', category='error')
            elif password1 != password2:
                  flash('Both password is not same', category='success')
            else:
                  new_user = User(email = email, first_name = first_name, password = generate_password_hash(password1, method='scrypt'))
                  db.session.add(new_user)
                  db.session.commit()
                  flash('Account created', category='success')
                  return redirect(url_for('auth.login'))
      return render_template('signUp.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
      logout_user()
      flash('logout successfully', category='success')
      return redirect(url_for('auth.login'))

