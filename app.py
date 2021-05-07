from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user


app = Flask(__name__, template_folder="pages")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'soFDSFSnajnwYajd138f1a9f4984@°ç°*:°*FGsef'
app.config['DEBUG'] = True

db = SQLAlchemy(app)

login_manager = LoginManager(app)

# Definisco la classe User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20))

    def __repr__(self):
        return '<User %r>' % self.username
    
    def is_active(self):
       return True
       
    def get_id(self):
        return (self.id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('usernane required'), Length(max=80, message="nome lungo")])
    email = StringField('email', validators=[InputRequired('email required'), Length(max=80, message="email longe")])
    password = PasswordField('password', validators=[InputRequired('pass required')]) 



class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')



@app.route('/')
def index():
    if request.method == 'GET':
        return render_template("sign-up.html")

@app.route('/login', methods=['GET', 'POST'])
def login():




    return render_template('sign-in.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
 
        return '<h1> Name: {}, email: {} </h1>'.format(form.username.data, form.email.data)


    return render_template("registration.html", form=form)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)