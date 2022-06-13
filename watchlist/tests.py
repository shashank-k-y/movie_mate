from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from watchlist.models import StreamingPlatform


class TestStreamPlatform(APITestCase):

    def setUp(self):
        User.objects.create_user(username='django', password='testpass')
        self.token = Token.objects.get(user__username='django')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.path = reverse('platform')
        self.platform = StreamingPlatform.objects.create(
            name='netflix',
            about='movies and series',
            website='http://www.netflix.com'
        )

    def test_create_stream_platform_non_staff_user(self):
        data = {
            "name": "Hulu",
            "about": "watch for good movies",
            "website": "http://www.hulu.com"
        }
        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()['detail'],
            'You do not have permission to perform this action.'
        )

    def test_get_stream_platform_staff_user(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()[0]
        self.assertEqual(json_response['name'], self.platform.name)
        self.assertEqual(json_response['about'], self.platform.about)
        self.assertEqual(json_response['website'], self.platform.website)

    def test_get_individual_stream_platform_item(self):
        response = self.client.get(
            path=reverse("platform", args=(self.platform.id,))
        )
        json_response = response.json()
        self.assertEqual(json_response['name'], self.platform.name)
        self.assertEqual(json_response['about'], self.platform.about)
        self.assertEqual(json_response['website'], self.platform.website)

    def test_create_streaming_platform_staff_user(self):
        data = {
            "name": "Hulu",
            "about": "watch for good movies",
            "website": "http://www.hulu.com"
        }
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        response = self.client.post(path=self.path, data=data)
        platform = StreamingPlatform.objects.get(name='Hulu')
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['name'], platform.name)
        self.assertEqual(json_response['about'], platform.about)
        self.assertEqual(json_response['website'], platform.website)
