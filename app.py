import os
from flask import Flask,render_template, redirect, url_for, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_user=os.environ.get('DB_USER')
db_host=os.environ.get('DB_HOST')
db_password=os.environ.get('DB_PASSWORD')
db_name=os.environ.get('DB_NAME')

app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:@localhost/permission'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECURITY_PASSWORD_SALT']="MY_SECRET"
app.config['SECURITY_REGISTRABLE']=True
app.config['SECURITY_SEND_REGISTER_EMAIL']=False

from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()


from flask_security import UserMixin, RoleMixin

roles_users= db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
                     
class User(db.Model, UserMixin):
    __tablename__= 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref='roled')

class Role(db.Model, UserMixin):
    __tablename__= 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name= db.Column(db.String(80), unique=True)

@app.before_first_request
def create_tables():
    db.create_all()

from flask_login import LoginManager, login_manager, login_user
from flask_security import Security, SQLAlchemySessionUserDatastore


@app.route('/')
def index():
    return render_template("index.html")

# signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg=""
    # if the form is submitted
    if request.method == 'POST':
    # check if user already exists
        user = User.query.filter_by(email=request.form['email']).first()
        msg=""
        # if user already exists render the msg
        if user:
            msg="User already exist"
            # render signup.html if user exists
            return render_template('signup.html', msg=msg)
        
        # if user doesn't exist
        
        # store the user to database
        user = User(email=request.form['email'], active=1, password=request.form['password'])
        # store the role
        role = Role.query.filter_by(id=request.form['options']).first()
        user.roles.append(role)
        
        # commit the changes to database
        db.session.add(user)
        db.session.commit()
        
        # login the user to the app
        # this user is current user
        login_user(user)
        # redirect to index page
        return redirect(url_for('index'))
        
    # case other than submitting form, like loading the page itself
    else:
        return render_template("signup.html", msg=msg)

# signin page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg=""
    if request.method == 'POST':
        # search user in database
        user = User.query.filter_by(email=request.form['email']).first()
        # if exist check password
        if user:
            if  user.password == request.form['password']:
                # if password matches, login the user
                login_user(user)
                return redirect(url_for('index'))
            # if password doesn't match
            else:
                msg="Wrong password"
        
        # if user does not exist
        else:
            msg="User doesn't exist"
        return render_template('signin.html', msg=msg)
        
    else:
        return render_template("signin.html", msg=msg)


