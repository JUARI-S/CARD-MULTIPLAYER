from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/online_28/lobby', consumers.LobbyConsumer.as_asgi()),
    re_path(r'ws/online_28/arena', consumers.GameConsumer.as_asgi())
]