from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from ecosystem.models import User, Post, Poll, Event, Item

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20) ])
    apt_no = IntegerField('Apartment Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if(user):
            raise ValidationError('Username taken')
    def validate_apt_no(self, apt_no):
        user = User.query.filter_by(apt_no=apt_no.data).first()
        if(user):
            raise ValidationError('That Apartment Already Has An Account ')
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20) ])
    apt_no = IntegerField('Apartment Number', validators=[DataRequired()])
    submit = SubmitField('Update')
    def validate_username(self, username):
        if(username.data != current_user.username):
            user = User.query.filter_by(username=username.data).first()
            if(user):
                raise ValidationError('Username taken')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    go_anonymous = BooleanField('Post Anomymously')
    submit = SubmitField('Post')

class EventForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired(), Length(min = 4, max = 25)])
    date_of_event = StringField('Date of event', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    submit = SubmitField('Post')

class CreatePollForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired()])
    option1 = StringField('Option1', validators=[DataRequired()])
    option2 = StringField('Option2', validators=[DataRequired()])
    submit = SubmitField('Create Poll')

class VoteForm(FlaskForm):
    vote_1 = BooleanField('Vote for option 1')
    vote_2 = BooleanField('Vote for option 2')
    submit = SubmitField('Submit Vote')

class SearchForm(FlaskForm):
    search = StringField('Enter apartment number', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Search')

class FoundItemForm(FlaskForm):
    description = TextAreaField('Description')
    submit = SubmitField('Submit')



