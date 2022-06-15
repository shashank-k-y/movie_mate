from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from watchlist.models import StreamingPlatform, WatchList


class TestStreamPlatform(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='django', password='testpass'
        )
        self.token, self.created = Token.objects.get_or_create(
            user_id=self.user.id
        )
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

    def test_update_individual_stream_platform_item(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        data = {
            "name": "Hulu",
            "about": "series and movies",
            "website": "http://www.hulu.com"
        }
        response = self.client.put(
            path=reverse("platform", args=(self.platform.id,)),
            data=data
        )
        platform = StreamingPlatform.objects.get(id=self.platform.id)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["name"], platform.name)
        self.assertEqual(json_response["about"], platform.about)
        self.assertEqual(json_response["website"], platform.website)

    def test_update_individual_stream_platform_item_missing_fields(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        response = self.client.put(
            path=reverse("platform", args=(self.platform.id,)),
            data={"name": "Hulu", "about": "series and movies"}
        )
        json_response = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json_response["website"][0], 'This field is required.'
        )

    def test_update_individual_stream_platform_object_doesnot_exist(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        response = self.client.put(
            path=reverse("platform", args=(2,)),
            data={"name": "Hulu", "about": "series and movies"}
        )
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response["error"], 'Platform does not exist')

    def test_delete_individual_stream_platform_item(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        response = self.client.delete(
            path=reverse("platform", args=(self.platform.id,))
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_individual_stream_platform_item_not_found(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        response = self.client.delete(
            path=reverse("platform", args=(3,))
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Platform does not exist")


class TestWatchList(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='django', password='testpass'
        )
        self.token, self.created = Token.objects.get_or_create(
            user_id=self.user.id
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.path = reverse('list')
        self.platform = StreamingPlatform.objects.create(
            name='netflix',
            about='movies and series',
            website='http://www.netflix.com'
        )
        self.movie_data = {
            "platform": self.platform,
            "title": 'dummy-movie',
            "storyline": 'dummy storyline',
            "active": True
        }
        self.movie = WatchList.objects.create(**self.movie_data)

    def test_create_watchlist_non_staff_user(self):
        data = {
            "platform": self.platform,
            "title": 'test movie',
            "storyline": 'test storyline',
            "active": True
        }
        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_watchlist_staff_user(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        data = {
            "platform": self.platform,
            "title": 'test movie',
            "storyline": 'test storyline',
            "active": True
        }
        response = self.client.post(path=self.path, data=data)
        movie = WatchList.objects.get(title='test movie')
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["platform"], movie.platform.name)
        self.assertEqual(json_response["title"], movie.title)
        self.assertEqual(json_response["storyline"], movie.storyline)

    def test_get_watchlist(self):
        response = self.client.get(path=self.path)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 1)
        self.assertEqual(
            json_response[0]['platform'], self.movie.platform.name
        )
        self.assertEqual(json_response[0]['title'], self.movie.title)
        self.assertEqual(json_response[0]['storyline'], self.movie.storyline)

    def test_get_watchlist_movie_not_found(self):
        response = self.client.get(
            path=reverse("movie_detail", args=(3,))
        )
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response['error'], 'Movie does not exist')

    def test_update_watch_list_movie_not_found(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        data = {
            "platform": self.platform,
            "title": 'test update movie',
            "storyline": 'test update storyline',
            "active": True
        }
        response = self.client.put(
            path=reverse("movie_detail", args=(3,)),
            data=data
        )
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response['error'], 'Movie does not exist')

    def test_update_watch_list_movie(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        data = {
            "platform": self.platform,
            "title": 'test update movie',
            "storyline": 'test update storyline',
            "active": True
        }
        response = self.client.put(
            path=reverse("movie_detail", args=(self.movie.id,)),
            data=data
        )
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        self.assertEqual(json_response['title'], self.movie.title)
        self.assertEqual(json_response['storyline'], self.movie.storyline)
        self.assertEqual(json_response['active'], self.movie.active)

    def test_delete_watch_list_movie(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        response = self.client.delete(
            path=reverse("movie_detail", args=(self.movie.id,))
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_watch_list_movie_not_found(self):
        user = User.objects.get(username='django')
        user.is_staff = True
        user.save()
        response = self.client.delete(
            path=reverse("movie_detail", args=(3,))
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Movie does not exist')
