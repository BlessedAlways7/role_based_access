import os
from flask import Flask,render_template, redirect, url_for

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

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


db=SQLAlchemy()
db.init_app(app)
app.app_context().push()



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





