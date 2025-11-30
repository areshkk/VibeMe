from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
import re


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Связь "один ко многим" с MoodEntry
    mood_entries = db.relationship('MoodEntry', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Дополнительная валидация при создании
        if self.email:
            self.email = self.email.lower().strip()
        if self.username:
            self.username = self.username.strip()

    def set_password(self, password):
        """Хеширование пароля с использованием современного алгоритма"""
        if len(password) < 8:
            raise ValueError('Пароль должен быть не менее 8 символов')
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', password):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву, одну строчную и одну цифру')

        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )

    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        super(MoodEntry, self).__init__(**kwargs)
        # Валидация настроения
        valid_moods = ['happy', 'calm', 'neutral', 'sad', 'angry', 'anxious', 'excited', 'tired']
        if self.mood and self.mood not in valid_moods:
            raise ValueError(f"Invalid mood: {self.mood}")

    def __repr__(self):
        return f'<MoodEntry {self.mood} by {self.author.username}>'