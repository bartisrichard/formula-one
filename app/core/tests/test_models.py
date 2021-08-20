from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@acetech.dev', password='testpass'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@acetech.dev'
        password = 'Password123'
        user = get_user_model().objects.create_user(
			email=email,
			password=password
		)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'test@AECETECH.dev'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@acetech.dev',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_car_str(self):
        car = models.Car.objects.create(
            user=sample_user(),
            name='Alpine_A521',
            enginesupplier='Renault',
            performance=72,
            wear=32,
        )

        self.assertEqual(str(car), car.name)
