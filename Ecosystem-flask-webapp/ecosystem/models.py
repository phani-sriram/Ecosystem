from datetime import datetime
from ecosystem import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    apt_no = db.Column(db.String(3), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    events = db.relationship('Event', backref='author', lazy=True)
    polls = db.relationship('Poll', backref='author', lazy=True)
    #voted_polls = db.relationship('Poll', backref='voter', lazy=True)
    #poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.apt_no}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable= False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anonymity = db.Column(db.Boolean, default = False)
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(30), nullable=False)
    date_of_event = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Event('{self.category}', '{self.date_of_event}')"

'''class Option(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable=False, unique=True)
    no_of_votes = db.Column(db.Integer)
    def __repr__(self):
        return f"Option('{self.name}', '{self.no_of_votes}')"'''

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    votes_1 = db.Column(db.Integer, nullable=False)
    votes_2 = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Poll('{self.option1}', '{self.option2}', '{self.date_posted}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    def __repr__(self):
        return f"Item('{self.category}')"



