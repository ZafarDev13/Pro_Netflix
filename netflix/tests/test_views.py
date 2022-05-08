from django.test import TestCase, Client

from netflix.models import Movie, Actor


class TestMovieViewSet(TestCase):
    def setUp(self) -> None:
        self.movie = Movie.objects.create(name="Test1 movie name", year='2022-12-12', imdb=1, genre='Drama')
        self.movie = Movie.objects.create(name="Test2 movie name", year='2022-12-12', imdb=5, genre='Drama')
        self.client = Client()

    def test_get_list_movie(self):
        response = self.client.get('/v1/movies/')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertIsNotNone(data[0]["id"])
        self.assertEqual(data[0]['name'], "Test1 movie name")
        self.assertEqual(data[0]['year'], "2022-12-12")
        self.assertEqual(data[0]['imdb'], 1)
        self.assertEqual(data[0]['genre'], "Drama")
        self.assertEqual(data[0]['actors'], [])


    def test_search(self):
        response = self.client.get('/v1/movies/?search=Test')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Test1 movie name")

    def test_ordering(self):
        response = self.client.get('/v1/movies/?ordering=-imdb')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['imdb'], 5)
        print(f"**********{data}")
