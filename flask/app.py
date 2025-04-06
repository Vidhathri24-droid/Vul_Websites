from flask import Flask, render_template, url_for, request, flash, redirect, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from flask_wtf.file import FileAllowed
import os
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my_db_password@localhost/my_db?auth_plugin=mysql_native_password'
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)
        is_admin = db.Column(db.Boolean, default=False)
        image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

        def __repr__(self):
                return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class blogs(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        content = db.Column(db.Text, nullable=False)
        author = db.Column(db.String(100), nullable=False)
        date_posted = db.Column(db.DateTime, default=datetime.utcnow)
        def __repr__(self):
                return '<BlogPost %r>' % self.title

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
        username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
        email = StringField('Email', validators=[DataRequired(), Email()])
        picture = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg','png'])])
        submit = SubmitField('Update')

class PostForm(FlaskForm):
        title = StringField('Title:', validators=[DataRequired()])
        content = StringField('Content:', validators=[DataRequired()])
        author = StringField('Author:', validators=[DataRequired()])
        submit = SubmitField('Submit')

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

@app.route('/')
def index():
        posts = blogs.query.order_by(blogs.date_posted.desc()).all()
        return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user =User(username=form.username.data,email=form.email.data,password=hashed_password)
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
                user = User.query.filter_by(email=form.email.data).first()
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


@app.route('/admin')
@login_required
def admin():
        if not current_user.is_admin:
                return redirect(url_for('index'))
        users = User.query.all()
        return render_template('admin.html', users=users)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
        if not current_user.is_admin:
                return redirect(url_for('home'))
        user = User.query.get(user_id)
        if user:
                if user.id == current_user.id:
                        flash('You cannot delete yourself!!')
                else:
                        db.session.delete(user)
                        db.session.commit()
                        flash('User has been deleted')
        return redirect(url_for('admin'))

@app.route('/delete_account', methods=['GET','POST'])
@login_required
def delete_account():
        if current_user.is_admin:
                flash('Admins cannot delete their accounts!!!')
                return redirect(url_for('index'))
        user = User.query.get(current_user.id)
        if user:
                db.session.delete(user)
                db.session.commit()
                flash('Your account has been deleted!!')
                return redirect(url_for('login'))
        else:
                flash('User not found')
                return redirect(url_for('index'))

def save_picture(form_picture):
        random_hex = os.urandom(8).hex()
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_fn)
        try:
                output_size = (125, 125)
                i = Image.open(form_picture)
                i.thumbnail(output_size)
                i.save(picture_path)
        except Exception as e:
                print(f"Error: {e}")

        return picture_fn


@app.route('/update', methods=['GET','POST'])
@login_required
def update():
        form = UpdateAccountForm()
        if form.validate_on_submit():
                if form.picture.data:
                        picture_file = save_picture(form.picture.data)
                        current_user.image_file = picture_file
                current_user.username = form.username.data
                current_user.email = form.email.data
                db.session.commit()
                flash('Your account has been updated!!!')
                return redirect(url_for('dashboard'))
        elif request.method == 'GET':
                form.username.data = current_user.username
                form.email.data = current_user.email
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('account.html', image_file=image_file, form=form)

@app.route('/add', methods=['POST', 'GET'])
def add():
        form = PostForm()
        if request.method == 'POST':
                title = request.form['title']
                content = request.form['content']
                author = request.form['author']
                new_post = blogs(title=title, content=content, author=author)
                try:
                        db.session.add(new_post)
                        db.session.commit()
                        return redirect('/')
                except:
                        return 'There was an issue adding your post'
        else:
                return render_template('add_post.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
        username = session.get('username', 'Guest')
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('dashboard.html', title='Dashboard', image_file=image_file)

if __name__ == "__main__":
        app.run(debug=True)
