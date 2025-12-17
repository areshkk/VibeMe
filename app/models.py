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
    # One-to-many relationship with MoodEntry
    mood_entries = db.relationship('MoodEntry', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Additional validation on creation
        if self.email:
            self.email = self.email.lower().strip()
        if self.username:
            self.username = self.username.strip()

    def set_password(self, password):
        """Hash password using modern algorithm"""
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', password):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter and one digit')

        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )

    def check_password(self, password):
        """Check password"""
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
        # Mood validation
        valid_moods = ['happy', 'calm', 'neutral', 'sad', 'angry', 'anxious', 'excited', 'tired']
        if self.mood and self.mood not in valid_moods:
            raise ValueError(f"Invalid mood: {self.mood}")

    def __repr__(self):
        return f'<MoodEntry {self.mood} by {self.author.username}>'


class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False, index=True)
    advice = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), default='general')
    priority = db.Column(db.Integer, default=1)  # Priority from 1 (high) to 5 (low)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Recommendation for {self.mood}: {self.advice[:50]}...>'


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Prediction {self.category}: {self.text[:50]}...>'