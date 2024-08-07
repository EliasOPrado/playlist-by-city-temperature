import requests
import logging
from django.conf import settings
from django.http import JsonResponse

# Set up logging
logger = logging.getLogger(__name__)

# Retrieve API keys from settings
WEATHER_API_KEY = settings.WEATHER_API_KEY
SPOTIFY_CLIENT_ID = settings.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET


def get_temperature_by_city(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Validate that 'main' and 'temp' keys exist
        if "main" in data and "temp" in data["main"]:
            temp = int(data["main"]["temp"] - 273.15)
            return JsonResponse(
                {"city": data["name"], "temperature": temp},
                json_dumps_params={"ensure_ascii": False},
            )
        else:
            logger.error("Unexpected response format: %s", data)
            return JsonResponse({"error": "Unexpected response format"}, status=500)

    except requests.exceptions.RequestException as e:
        logger.error("Error fetching weather data: %s", e)
        return JsonResponse(
            {"error": "Error fetching weather data"},
            status=response.status_code if response else 500,
        )


def get_spotify_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        response_data = response.json()

        # Check if access token is present
        if "access_token" in response_data:
            return response_data["access_token"]
        else:
            logger.error("Failed to retrieve access token: %s", response_data)
            return None

    except requests.exceptions.RequestException as e:
        logger.error("Error retrieving Spotify access token: %s", e)
        return None


def get_playlist_by_genre(genre):
    access_token = get_spotify_access_token()
    if not access_token:
        return JsonResponse(
            {"error": "Failed to retrieve Spotify access token"}, status=500
        )

    url = f"https://api.spotify.com/v1/search?q=genre:{genre}&type=album&limit=10"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Validate that 'albums' and 'items' keys exist
        if "albums" in data and "items" in data["albums"]:
            albums = [
                {
                    "name": album["name"],
                    "artist": album["artists"][0]["name"],
                    "release_date": album["release_date"],
                    "url": album["external_urls"]["spotify"],
                    "genre": genre,
                }
                for album in data["albums"]["items"]
            ]
            return JsonResponse(albums, safe=False)
        else:
            logger.error("Unexpected response format: %s", data)
            return JsonResponse({"error": "Unexpected response format"}, status=500)

    except requests.exceptions.RequestException as e:
        logger.error("Error fetching albums by genre: %s", e)
        return JsonResponse(
            {"error": "Failed to fetch albums by genre"},
            status=response.status_code if response else 500,
        )
