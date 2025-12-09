# config.py
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Базовые настройки
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production-2024'

    # Используем абсолютный путь к базе данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'vibeme.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Настройки безопасности
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    SESSION_PROTECTION = 'strong'

    # Настройки для production
    if os.environ.get('FLASK_ENV') == 'production':
        SESSION_COOKIE_SECURE = True
        REMEMBER_COOKIE_SECURE = True
        SESSION_COOKIE_HTTPONLY = True
        REMEMBER_COOKIE_HTTPONLY = True
        PREFERRED_URL_SCHEME = 'https'

    # Лимиты для защиты от brute-force
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_BAN_TIME = timedelta(minutes=15)