import re
from datetime import datetime, timedelta


class SecurityUtils:
    @staticmethod
    def is_strong_password(password):
        """
        Проверка сложности пароля
        """
        if len(password) < 8:
            return False, "Пароль должен быть не менее 8 символов"

        if not re.search(r'[a-z]', password):
            return False, "Пароль должен содержать хотя бы одну строчную букву"

        if not re.search(r'[A-Z]', password):
            return False, "Пароль должен содержать хотя бы одну заглавную букву"

        if not re.search(r'\d', password):
            return False, "Пароль должен содержать хотя бы одну цифру"

        return True, "Пароль надежен"

    @staticmethod
    def sanitize_input(text):
        """
        Базовая очистка пользовательского ввода
        """
        if not text:
            return text

        # Удаляем потенциально опасные символы
        sanitized = re.sub(r'[<>&\"\']', '', text)
        return sanitized.strip()

    @staticmethod
    def validate_username(username):
        """
        Валидация имени пользователя
        """
        if not username:
            return False, "Имя пользователя не может быть пустым"

        if len(username) < 3 or len(username) > 64:
            return False, "Имя пользователя должно быть от 3 до 64 символов"

        if not re.match(r'^[A-Za-zА-Яа-я0-9_]+$', username):
            return False, "Имя пользователя может содержать только буквы, цифры и подчеркивания"

        return True, "Имя пользователя корректно"