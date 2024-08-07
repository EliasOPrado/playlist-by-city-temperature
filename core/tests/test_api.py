from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status


class TestEndpoints(TestCase):

    @patch('core.views.get_temperature_by_city')
    @patch('core.views.get_playlist_by_genre')
    def test_get_playlist_by_city_temperature(self, mock_get_playlist, mock_get_temperature):

        mock_get_temperature.return_value = {"city": "London", "temperature": 15}

        mock_get_playlist.return_value = [
            {
                "name": "Rock Album",
                "artist": "Rock Artist",
                "release_date": "2021-01-01",
                "url": "https://open.spotify.com/album/rock",
                "genre": "rock",
            }
        ]

        url = reverse('playlist-by-city-temperature', args=['London'])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mock_get_temperature.assert_called_once_with('London')
        mock_get_playlist.assert_called_once_with('rock')

        response_data = response.json()

        self.assertIn('city', response_data)
        self.assertIn('temperature', response_data)
        self.assertIn('genre', response_data)
        self.assertIn('playlists', response_data)
        self.assertEqual(response_data['city'], 'London')
        self.assertEqual(response_data['temperature'], "15 degree celcius")
        self.assertEqual(response_data['genre'], 'rock')
        self.assertEqual(len(response_data['playlists']), 1)
        self.assertEqual(response_data['playlists'][0]['name'], 'Rock Album')
