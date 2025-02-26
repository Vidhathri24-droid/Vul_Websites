from flask import Flask, render_template, url_for, request, flash, redirect, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/db_name?auth_plugin=mysql_native_password'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Users(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)
        is_admin = db.Column(db.Boolean, default=False)
        def __repr__(self):
                return f"User('{self.id}','{self.username}', '{self.email}')"

class RegistrationForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
        submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
        username = StringField('Username')
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(),EqualTo('password',message="Passwords doesn't match")])
        submit = SubmitField('Update')

@login_manager.user_loader
def load_user(user_id):
        return Users.query.get(int(user_id))

@app.route('/')
def index():
        if not current_user.is_authenticated:
                return redirect(url_for('login'))
        else:
                return render_template('index1.html')

@app.route('/register', methods=['GET','POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user =Users(username=form.username.data,email=form.email.data,password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash('Your account created successfully!!!')
                return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
                user = Users.query.filter_by(email=form.email.data).first()
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                        login_user(user, remember=True)
                        session['username'] = user.username
                        return redirect(url_for('index'))
                else:
                        flash('Login Unsuccessful. Please Check email and password')
        return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
        logout_user()
        session.pop('username',None)
        return redirect(url_for('login'))

@app.route('/user')
def user():
        id = current_user.id
        return redirect(f"/dashboard/user_id={id}")

@app.route('/dashboard/user_id=<user_id>')
def dashboard(user_id):
        users = Users.query.filter_by(id=user_id).first()
        username = users.username
        email = users.email
        return render_template('dashboard.html',username=username, email=email)

@app.route('/update', methods=['GET','POST'])
def update():
        form = UpdateAccountForm()
        if form.validate_on_submit():
                current_user.username = form.username.data
                current_user.email = form.email.data
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                current_user.password = hashed_password
                try:
                        db.session.commit()
                        flash('Your account has been updated!!!')
                except Exception as e:
                        db.session.rollback()
                        flash("Error!! Your hasn't been updated")
                        print(f"Error : {e}")
                id = current_user.id
                return redirect(f"/dashboard/user_id={id}")
        else:
                print ("Form is not valid")
                print (form.errors)
                form.username.data = current_user.username
                form.email.data = current_user.email
        return render_template('account.html', form=form)

if __name__ == '__main__':
        app.run(debug=True)          
          
