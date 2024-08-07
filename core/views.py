from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from core.services import get_temperature_by_city, get_playlist_by_genre


class PlaylistByCityTemperatureAPIView(APIView):
    def get(self, request, city, format=None):

        temp_data = get_temperature_by_city(city)

        if "error" in temp_data:
            return Response(temp_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        temperature = temp_data["temperature"]

        match temperature:
            case t if t > 25:
                genre = "pop"
            case t if 10 <= t <= 25:
                genre = "rock"
            case t if t < 10:
                genre = "classical"

        playlists = get_playlist_by_genre(genre)

        if "error" in playlists:
            return Response(playlists, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {
                "city": city,
                "temperature": f"{temperature} degree celcius",
                "genre": genre,
                "playlists": playlists,
            },
            status=status.HTTP_200_OK,
        )
