from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email"""
        email = 'daniel@gmail.com'
        password = 'Testpass1994'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test convert the email address to lowercase"""
        email = 'daniel@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'Testpass1994')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Testpass1994')

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'daniel@gmail.com',
            'Testpass1994'
            )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
