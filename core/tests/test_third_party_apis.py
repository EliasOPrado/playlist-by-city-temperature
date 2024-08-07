import json
from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from core.services import (
    get_temperature_by_city,
    get_spotify_access_token,
    get_playlist_by_genre,
)


class TestThirdPartyApis(TestCase):

    @patch("requests.get")
    def test_get_temperature_success(self, mock_get):
        # Mock response data for a successful weather API call
        # fom the inner request.
        mock_response = {"name": "São Paulo", "main": {"temp": 293.15}}  # 20°C
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Call the function
        response = get_temperature_by_city("São Paulo")

        # Validate the JSON response
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        # Decode and load JSON response content
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_data["city"], "São Paulo")
        self.assertEqual(response_data["temperature"], 20)

    @patch("requests.get")
    def test_get_temperature_unexpected_format(self, mock_get):
        # Mock response data with an unexpected format
        mock_response = {"name": "São Paulo", "main": {}}  # Missing 'temp' key
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Call the function
        response = get_temperature_by_city("São Paulo")

        # Validate the JSON response for error
        self.assertEqual(response.status_code, 500)
        self.assertIsInstance(response, JsonResponse)

        # Decode and load JSON response content
        response_data = json.loads(response.content.decode("utf-8"))

        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Unexpected response format")

    @patch("requests.post")
    def test_get_spotify_access_token_success(self, mock_post):
        # Mock response data for a successful token retrieval
        mock_response = {"access_token": "test_access_token"}
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        # Call the function
        access_token = get_spotify_access_token()

        # Validate the access token
        self.assertIsNotNone(access_token)
        self.assertEqual(access_token, "test_access_token")

    @patch("requests.post")
    def test_get_spotify_access_token_failure(self, mock_post):
        # Mock response for a failed token retrieval
        mock_response = {"error": "invalid_client"}
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = mock_response

        # Call the function
        access_token = get_spotify_access_token()

        # Validate the access token
        self.assertIsNone(access_token)

    @patch("core.services.get_spotify_access_token")
    @patch("requests.get")
    def test_get_playlist_by_genre_success(
        self, mock_get, mock_get_spotify_access_token
    ):
        # Mock the access token
        mock_get_spotify_access_token.return_value = "mock_access_token"

        # Mock a successful response from the Spotify API
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "albums": {
                "items": [
                    {
                        "name": "Genre: Boring Pop",
                        "artists": [{"name": "Pattawiguys"}],
                        "release_date": "2021-01-05",
                        "external_urls": {
                            "spotify": "https://open.spotify.com/album/1k10ygj300td8SxU56T4aG"
                        },
                    },
                    {
                        "name": "If You Were a Music Genre, You'd Be Basic Pop (Typical Heart-Brake)",
                        "artists": [{"name": "Typical Minority"}],
                        "release_date": "2019-08-12",
                        "external_urls": {
                            "spotify": "https://open.spotify.com/album/5xXQaRAeeur9ok67h5cgJB"
                        },
                    },
                ]
            }
        }
        mock_get.return_value = mock_response

        # Call the function
        response = get_playlist_by_genre("pop")

        # Assert the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "name": "Genre: Boring Pop",
                    "artist": "Pattawiguys",
                    "release_date": "2021-01-05",
                    "url": "https://open.spotify.com/album/1k10ygj300td8SxU56T4aG",
                    "genre": "pop",
                },
                {
                    "name": "If You Were a Music Genre, You'd Be Basic Pop (Typical Heart-Brake)",
                    "artist": "Typical Minority",
                    "release_date": "2019-08-12",
                    "url": "https://open.spotify.com/album/5xXQaRAeeur9ok67h5cgJB",
                    "genre": "pop",
                },
            ],
        )
