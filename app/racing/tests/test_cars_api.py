from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Car

from racing.serializers import CarSerializer


CARS_URL = reverse('racing:car-list')


class PublicCarsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCarsApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@acetech.dev',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_cars(self):
        Car.objects.create(user=self.user, name='Ferrari_SF90', enginesupplier='Ferrari', performance=83, wear=41)
        Car.objects.create(user=self.user, name='Alpine_A521', enginesupplier='Renault', performance=72, wear=32)

        res = self.client.get(CARS_URL)

        cars = Car.objects.all().order_by('-name')
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_cars_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'other@acetech.dev',
            'testpass'
        )
        Car.objects.create(user=user2, name='Red_Bull_Racing_RB16', enginesupplier='Honda', performance=95, wear=73)
        car = Car.objects.create(user=self.user, name='Mercedes_AMG_F1_W10', enginesupplier='Mercedes', performance=93, wear=38)

        res = self.client.get(CARS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], car.name)

    """def test_create_car_successful(self):
        payload = {'name': 'Simple'}
        self.client.post(CARS_URL, payload)

        exists = Car.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_car_invalid(self):
        payload = {'name': ''}
        res = self.client.post(CARS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)"""
