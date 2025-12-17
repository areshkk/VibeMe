import unittest
import os
import sys
from werkzeug.security import check_password_hash

# Add project path
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
        """Test password hashing"""
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('SecurePassword123')

            self.assertTrue(user.check_password('SecurePassword123'))
            self.assertFalse(user.check_password('WrongPassword'))

            # Check that password is actually hashed
            self.assertTrue(user.password_hash.startswith('pbkdf2:sha256:'))
            self.assertNotEqual(user.password_hash, 'SecurePassword123')

    def test_password_strength_validation(self):
        """Test password strength validation"""
        with self.app.app_context():
            user = User(username='testuser2', email='test2@example.com')

            # Weak password - only digits
            with self.assertRaises(ValueError):
                user.set_password('12345678')

            # Weak password - only letters
            with self.assertRaises(ValueError):
                user.set_password('Password')

            # Weak password - no uppercase
            with self.assertRaises(ValueError):
                user.set_password('password123')

            # Weak password - no digits
            with self.assertRaises(ValueError):
                user.set_password('Password')

            # Short password
            with self.assertRaises(ValueError):
                user.set_password('Pass1')

            # Good password
            try:
                user.set_password('SecurePassword123')
                self.assertTrue(True)  # If no exception
            except ValueError:
                self.fail("Valid password raised ValueError")

    def test_user_creation_validation(self):
        """Test validation on user creation"""
        with self.app.app_context():
            # Valid user
            user = User(username='valid_user', email='valid@example.com')
            user.set_password('ValidPass123')
            db.session.add(user)
            db.session.commit()

            self.assertIsNotNone(User.query.filter_by(username='valid_user').first())

    def test_email_normalization(self):
        """Test email normalization"""
        with self.app.app_context():
            user = User(username='testuser3', email='  TEST@EXAMPLE.COM  ')
            user.set_password('TestPass123')
            db.session.add(user)
            db.session.commit()

            saved_user = User.query.filter_by(username='testuser3').first()
            self.assertEqual(saved_user.email, 'test@example.com')


if __name__ == '__main__':
    unittest.main()