from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@acetech.dev', password='testpass'):
    return get_user_model().objects.create_user(email, password)

"""def sample_car(name='Sample Car',enginesupplier='Sample Company',performance=50,wear=50):
    return get_car_model().objects.create_car(name, enginesupplier, performance, wear)

def sample_rating(name="sample rating",overall=50,experience=50,racecraft=50,awareness=50,pace=50):
    return get_rating_model().objects.create_rating(name, overall, experience, racecraft, awareness, pace)"""


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

    def test_rating_str(self):
        rating = models.Rating.objects.create(
            user=sample_user(),
            name="carlos_sainz_rating",
            overall=87,
            experience=69,
            racecraft=88,
            awareness=94,
            pace=85,
        )

        self.assertEqual(str(rating), rating.name)

    """def test_driver_str(self):
        driver = models.Driver.objects.create(
            user=sample_user(),
            name = "Carlos_Sainz",
            salaryinmill = 10,
            nationality = "Spanish",
            car = sample_car(),
            rating = sample_rating(),
        )

        self.assertEqual(str(driver), driver.title)"""
