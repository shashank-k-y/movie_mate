from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

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

    def test_user_already_exists(self):
        url = reverse('register')
        data = {
            "username": "django-user",
            "email": "django@test.com",
            "password": "testpassword",
            "password_2": "testpassword"
        }
        User.objects.create_user(
            username='django-user',
            password='testpassword',
            email="django@test.com"
        )
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()[0], 'User with the given email already exists'
        )


class TestLogin(APITestCase):

    def setUp(self):
        User.objects.create_user(username='django', password='testpass')

    def test_successfull_login(self):
        url = reverse('login')
        data = {
            "username": "django",
            "password": "testpass"
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessfull_login(self):
        url = reverse('login')
        data = {
            "username": "djangoooo",
            "password": "testpass"
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['non_field_errors'][0],
            'Unable to log in with provided credentials.'
        )


class TestLogOut(APITestCase):

    def setUp(self):
        User.objects.create_user(username='django', password='testpass')

    def test_successfull_logout(self):
        self.token = Token.objects.get(user__username='django')
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(path=url)
        self.assertEqual(response.status_code, 200)
