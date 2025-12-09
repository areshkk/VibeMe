from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя',
                          validators=[
                              DataRequired(message='Это поле обязательно'),
                              Length(min=3, max=64, message='Имя должно быть от 3 до 64 символов'),
                              Regexp('^[A-Za-zА-Яа-я0-9_]+$',
                                   message='Имя пользователя может содержать только буквы, цифры и подчеркивания')
                          ])
    email = StringField('Email',
                       validators=[
                           DataRequired(message='Это поле обязательно'),
                           Email(message='Введите корректный email адрес'),
                           Length(max=120, message='Email не должен превышать 120 символов')
                       ])
    password = PasswordField('Пароль',
                            validators=[
                                DataRequired(message='Это поле обязательно'),
                                Length(min=8, message='Пароль должен быть не менее 8 символов'),
                                Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)',
                                     message='Пароль должен содержать хотя бы одну заглавную букву, одну строчную и одну цифру')
                            ])
    confirm_password = PasswordField('Подтвердите пароль',
                                   validators=[DataRequired(message='Это поле обязательно'),
                                               EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято. Выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован. Используйте другой.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                       validators=[
                           DataRequired(message='Это поле обязательно'),
                           Email(message='Введите корректный email адрес')
                       ])
    password = PasswordField('Пароль',
                            validators=[
                                DataRequired(message='Это поле обязательно'),
                                Length(min=1, message='Введите пароль')
                            ])
    submit = SubmitField('Войти')

class MoodForm(FlaskForm):
    mood = SelectField('Настроение',
                      choices=[
                          ('happy', '😊 Счастлив'),
                          ('calm', '😌 Спокоен'),
                          ('neutral', '😐 Нейтрален'),
                          ('sad', '😔 Грустен'),
                          ('angry', '😠 Сердит'),
                          ('anxious', '😰 Тревожен'),
                          ('excited', '🎉 В восторге'),
                          ('tired', '😴 Устал')
                      ],
                      validators=[DataRequired(message='Выберите ваше настроение')])
    notes = TextAreaField('Заметки',
                         validators=[Length(max=500, message='Заметка не должна превышать 500 символов')])
    submit = SubmitField('Сохранить настроение')