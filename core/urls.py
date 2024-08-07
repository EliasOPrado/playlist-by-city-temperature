from django.urls import path
from core.views import PlaylistByCityTemperatureAPIView
from .views import get_temperature_by_city, get_playlist_by_genre

urlpatterns = [
    path(
        "api/playlist/<str:city>/",
        PlaylistByCityTemperatureAPIView.as_view(),
        name="playlist-by-city-temperature",
    ),
]
