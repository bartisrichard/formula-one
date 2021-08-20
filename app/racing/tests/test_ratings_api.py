from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Rating

from racing.serializers import RatingSerializer


RATINGS_URL = reverse('racing:rating-list')


class PublicRatingsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(RATINGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRatingsAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@acetech.dev',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_rating_list(self):
        Rating.objects.create(user=self.user, name='carlos_sainz_rating', overall=87, experience=69, racecraft=88, awareness=94, pace=85)
        Rating.objects.create(user=self.user, name='fernando_alonso_rating', overall=89, experience=99, racecraft=89, awareness=94, pace=86)

        res = self.client.get(RATINGS_URL)

        ratings = Rating.objects.all().order_by('-name')
        serializer = RatingSerializer(ratings, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ratings_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'other@acetech.dev',
            'testpass'
        )
        Rating.objects.create(user=user2, name='carlos_sainz_rating', overall=87, experience=69, racecraft=88, awareness=94, pace=85)

        rating = Rating.objects.create(user=self.user, name='fernando_alonso_rating', overall=89, experience=99, racecraft=89, awareness=94, pace=86)

        res = self.client.get(RATINGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], rating.name)

    """def test_create_ingredient_successful(self):
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)"""
