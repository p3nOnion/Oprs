from django.urls import path
from Terminal.tools.channel import websocket


websocket_urlpatterns = [
    path('webssh/', websocket.WebSSH),
]