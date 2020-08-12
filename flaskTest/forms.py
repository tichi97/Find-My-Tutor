from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flaskTest.models import User
from flask_login import current_user
import pycountry
STATES_A = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
          "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
          "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
          "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI",
          "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV",
          "WY"]
states=[]
for s in STATES_A:
    x=(s,s)
    states.append(x)
class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.alpha_2, country.name) for country in pycountry.countries]

class RegistrationForm(FlaskForm):
    
    username = StringField('Name',validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    location = SelectField('State you are based in', choices=states,validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
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

    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Name',
                           validators=[InputRequired(), Length(min=2, max=20)])
    location = SelectField('State you are based in', choices=states,validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken, please choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken, please choose another one')


class PostForm(FlaskForm):
    
    subject = SelectField('Main subject that you will tutor in',choices=[('Math','Math'),('English','English'),('Science','Science'),('Social Studies','Social Studies'),('Geography','Geography'),('Foreign Languages','Foreign Languages')],
                        validators=[InputRequired()])
    # subtopics=StringField('Sub-topics that you can tutor in',validators=[InputRequired()])
    topics = StringField('Sub-topics that you tutor in',validators=[InputRequired()])
    
    grades = SelectField('Grade levels that you teach', choices=[('K-5','K-5'), ('6-8','6-8'), ('9-12','9-12')],validators=[InputRequired()])
    style = TextAreaField('Description of your teaching style', validators=[InputRequired()])
    submit = SubmitField('Post')


class ContactForm(FlaskForm):
    name = StringField('Name',
                       validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    message = TextAreaField(
        'Tell the tutor a bit about yourself', validators=[InputRequired()])
    submit = SubmitField('Send')


class SearchForm(FlaskForm):
    search = StringField('', validators=[InputRequired()])
    submit = SubmitField('Search')
