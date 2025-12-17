import re
from datetime import datetime, timedelta


class SecurityUtils:
    @staticmethod
    def is_strong_password(password):
        """
        Check password strength
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"

        return True, "Password is strong"

    @staticmethod
    def sanitize_input(text):
        """
        Basic input sanitization
        """
        if not text:
            return text

        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>&\"\']', '', text)
        return sanitized.strip()

    @staticmethod
    def validate_username(username):
        """
        Username validation
        """
        if not username:
            return False, "Username cannot be empty"

        if len(username) < 3 or len(username) > 64:
            return False, "Username must be between 3 and 64 characters"

        if not re.match(r'^[A-Za-zА-Яа-я0-9_]+$', username):
            return False, "Username can only contain letters, numbers and underscores"

        return True, "Username is valid"