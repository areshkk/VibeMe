from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                          validators=[
                              DataRequired(message='This field is required'),
                              Length(min=3, max=64, message='Username must be between 3 and 64 characters'),
                              Regexp('^[A-Za-zА-Яа-я0-9_]+$',
                                   message='Username can only contain letters, numbers and underscores')
                          ])
    email = StringField('Email',
                       validators=[
                           DataRequired(message='This field is required'),
                           Email(message='Please enter a valid email address'),
                           Length(max=120, message='Email must not exceed 120 characters')
                       ])
    password = PasswordField('Password',
                            validators=[
                                DataRequired(message='This field is required'),
                                Length(min=8, message='Password must be at least 8 characters'),
                                Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)',
                                     message='Password must contain at least one uppercase letter, one lowercase letter and one digit')
                            ])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(message='This field is required'),
                                               EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please use another.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                       validators=[
                           DataRequired(message='This field is required'),
                           Email(message='Please enter a valid email address')
                       ])
    password = PasswordField('Password',
                            validators=[
                                DataRequired(message='This field is required'),
                                Length(min=1, message='Please enter your password')
                            ])
    submit = SubmitField('Login')

class MoodForm(FlaskForm):
    mood = SelectField('Mood',
                      choices=[
                          ('happy', '😊 Happy'),
                          ('calm', '😌 Calm'),
                          ('neutral', '😐 Neutral'),
                          ('sad', '😔 Sad'),
                          ('angry', '😠 Angry'),
                          ('anxious', '😰 Anxious'),
                          ('excited', '🎉 Excited'),
                          ('tired', '😴 Tired')
                      ],
                      validators=[DataRequired(message='Please select your mood')])
    notes = TextAreaField('Notes',
                         validators=[Length(max=500, message='Note must not exceed 500 characters')])
    submit = SubmitField('Save Mood')