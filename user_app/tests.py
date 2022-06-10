from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User


class TestRegistrationTestCases(APITestCase):

    def test_create_account(self):
        url = reverse('register')
        data = {
            "username": "django-user",
            "email": "django@test.com",
            "password": "testpassword",
            "password_2": "testpassword"
        }
        response = self.client.post(path=url, data=data, format='json')
        user = User.objects.get(username="django-user")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()['message'], 'django-user Succesfully registerd !'
        )
        self.assertEqual(user.username, 'django-user')
        self.assertEqual(user.email, 'django@test.com')

    def test_create_account_password_not_matching(self):
        url = reverse('register')
        data = {
            "username": "django-user",
            "email": "django@test.com",
            "password": "testpassword",
            "password_2": "test"
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], "Password didn't match")

    def test_create_account_without_fields(self):
        url = reverse('register')
        data = {
            "email": "django@test.com",
            "password": "testpassword",
            "password_2": "testpassword"
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['username'][0], 'This field is required.'
        )
