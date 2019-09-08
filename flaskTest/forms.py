from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskTest.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken, please choose another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken, please choose another one')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken, please choose another one')

    def validate_email(self, username):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken, please choose another one')


class PostForm(FlaskForm):
    title = StringField('Subject that you will tutor in',
                        validators=[DataRequired()])
    times = StringField('Days and Times that you are free',
                        validators=[DataRequired()])
    location = StringField('Locaiton - city,town,etc',
                           validators=[DataRequired()])
    experience = StringField('Experience tutoring eg. 6 months',
                             validators=[DataRequired()])
    content = TextAreaField(
        'Description of your teaching style', validators=[DataRequired()])
    submit = SubmitField('Post')


class ContactForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField(
        'Tell the tutor a bit about yourself', validators=[DataRequired()])
    submit = SubmitField('Send')


class SearchForm(FlaskForm):
    search = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search')
