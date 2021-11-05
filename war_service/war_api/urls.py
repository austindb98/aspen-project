from django.urls import include, path
from django.http import HttpResponse
from .views import *

urlpatterns = [
    path("createplayer/", create_player),
    path("getwins/", get_wins),
    path("getallwins/", get_all_wins),
    path("getgames/", get_games),
    path("startgame/", start_game),
    path("taketurn/", take_turn),
    path("playgame/", play_game),
    path("", lambda x: HttpResponse("<html>Service running!</html>"))
]
