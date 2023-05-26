from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

bcrypt = Bcrypt()

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(length=20), unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        pwd_hash = bcrypt.generate_password_hash(password)
        hashed_utf8 = pwd_hash.decode('utf8')

        return cls(username=username, password=hashed_utf8,  email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(length=100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username'))

    user = db.relationship('User', backref='feedback')