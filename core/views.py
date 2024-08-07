import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services import get_temperature_by_city, get_playlist_by_genre

logger = logging.getLogger(__name__)


class PlaylistByCityTemperatureAPIView(APIView):
    def get(self, request, city, format=None):

        temp_data = get_temperature_by_city(city)

        if not temp_data or "temperature" not in temp_data:
            error_message = temp_data.get("error", "No temperature data returned")
            logger.error(f"Temperature service error: {error_message}")
            return Response(
                {
                    "error": f"Failed to retrieve temperature data for {city}: {error_message}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        temperature = temp_data["temperature"]

        if temperature > 25:
            genre = "pop"
        elif 10 <= temperature <= 25:
            genre = "rock"
        elif temperature < 10:
            genre = "classical"

        playlists = get_playlist_by_genre(genre)

        if not playlists or not isinstance(playlists, list):
            logger.error(
                f"Playlist service error: No playlists data returned or incorrect format"
            )
            return Response(
                {
                    "error": f"Failed to retrieve playlists for genre {genre}: No playlists data returned or incorrect format"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "city": city,
                "temperature": f"{temperature} degree celcius",
                "genre": genre,
                "playlists": playlists,
            },
            status=status.HTTP_200_OK,
        )
