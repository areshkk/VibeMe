import unittest
import os
import sys
from werkzeug.security import check_password_hash

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User


class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_password_hashing(self):
        """Тестирование хеширования паролей"""
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('SecurePassword123')

            self.assertTrue(user.check_password('SecurePassword123'))
            self.assertFalse(user.check_password('WrongPassword'))

            # Проверяем, что пароль действительно хешируется
            self.assertTrue(user.password_hash.startswith('pbkdf2:sha256:'))
            self.assertNotEqual(user.password_hash, 'SecurePassword123')

    def test_password_strength_validation(self):
        """Тестирование проверки сложности пароля"""
        with self.app.app_context():
            user = User(username='testuser2', email='test2@example.com')

            # Слабый пароль - только цифры
            with self.assertRaises(ValueError):
                user.set_password('12345678')

            # Слабый пароль - только буквы
            with self.assertRaises(ValueError):
                user.set_password('Password')

            # Слабый пароль - без заглавных букв
            with self.assertRaises(ValueError):
                user.set_password('password123')

            # Слабый пароль - без цифр
            with self.assertRaises(ValueError):
                user.set_password('Password')

            # Короткий пароль
            with self.assertRaises(ValueError):
                user.set_password('Pass1')

            # Хороший пароль
            try:
                user.set_password('SecurePassword123')
                self.assertTrue(True)  # Если не было исключения
            except ValueError:
                self.fail("Valid password raised ValueError")

    def test_user_creation_validation(self):
        """Тестирование валидации при создании пользователя"""
        with self.app.app_context():
            # Корректный пользователь
            user = User(username='valid_user', email='valid@example.com')
            user.set_password('ValidPass123')
            db.session.add(user)
            db.session.commit()

            self.assertIsNotNone(User.query.filter_by(username='valid_user').first())

    def test_email_normalization(self):
        """Тестирование нормализации email"""
        with self.app.app_context():
            user = User(username='testuser3', email='  TEST@EXAMPLE.COM  ')
            user.set_password('TestPass123')
            db.session.add(user)
            db.session.commit()

            saved_user = User.query.filter_by(username='testuser3').first()
            self.assertEqual(saved_user.email, 'test@example.com')


if __name__ == '__main__':
    unittest.main()