from flask import Flask, render_template, url_for, redirect, request, flash, session, render_template_string, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:09082024@localhost/xss_vul?auth_plugin=mysql_native_password"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model,UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)
        is_admin = db.Column(db.Boolean, default=False)
        def __repr__(self):
                return f"User('{self.username}','{self.email}')"

class blogs(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        content = db.Column(db.Text, nullable=False)
        date_posted = db.Column(db.DateTime, default=datetime.utcnow)
        def __repr__(self):
                return '<BlogPost %r>' %self.title

class RegistrationForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        email = StringField('Email',validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
        submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Login')

class PostForm(FlaskForm):
        title = StringField('Title:', validators=[DataRequired()])
        content = StringField('Content:', validators=[DataRequired()])
        submit = SubmitField('Submit')

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

@app.route('/register', methods=['GET','POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(username=form.username.data, email=form.email.data, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash('User Registered Successfully')
                return redirect(url_for('login'))
        return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data).first()
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                        login_user(user, remember=True)
                        session['username'] = user.username
                        return redirect(url_for('search'))
                else:
                        flash('Login Unsuccessful. Incorrect Password')
        return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
        logout_user()
        session.pop('username',None)
        return redirect(url_for('login'))

comments = []

@app.route('/',methods=['GET','POST'])
@login_required
def home():
    return render_template('index.html')

@app.route('/search')
def search():
        query = request.args.get('query')
        return f'<h2>Results for:</h2><p> {query}<p>', 404

@app.route('/admin')
def admin_panel():
        resp = make_response('<h1>Admin Panel</h1>')
        resp.set_cookie('admin_cookie', '123235redc5terfsddeqa')
        return resp

if __name__ == '__main__':
    app.run(debug=True)
