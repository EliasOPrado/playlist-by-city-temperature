import requests
import logging
from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger(__name__)

WEATHER_API_KEY = settings.WEATHER_API_KEY
SPOTIFY_CLIENT_ID = settings.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET


def get_temperature_by_city(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "main" in data and "temp" in data["main"]:
            temp = int(data["main"]["temp"] - 273.15)
            return {"city": data["name"], "temperature": int(temp)}

        else:
            logger.error(f"Unexpected response format: {data}")
            return {"error": "Unexpected response format"}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return {"error": "Unexpected response format"}


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
        response.raise_for_status()
        response_data = response.json()

        if "access_token" in response_data:
            return response_data["access_token"]
        else:
            logger.error(f"Failed to retrieve access token: {response_data}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving Spotify access token: {e}")
        return None


def get_playlist_by_genre(genre):
    access_token = get_spotify_access_token()
    if not access_token:
        return {"error": "Failed to retrieve Spotify access token"}

    url = f"https://api.spotify.com/v1/search?q=genre:{genre}&type=album&limit=10"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

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
            return albums
        else:
            logger.error(f"Unexpected response format: {data}")
            return {"error": "Unexpected response format"}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching albums by genre: {e}")
        return JsonResponse(
            {"error": "Failed to fetch albums by genre"},
            status=response.status_code if response else 500,
        )
