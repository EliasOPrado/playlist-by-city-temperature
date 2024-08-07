from django.urls import path
from .views import get_temperature_by_city, get_playlist_by_genre

urlpatterns = [
    path("temperature/<str:city>/", get_temperature_by_city),
    path("albuns/<str:genre>", get_playlist_by_genre),
]
