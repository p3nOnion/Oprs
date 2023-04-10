from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# import app.routing
from django.urls import re_path, path

from django.urls import re_path

import Core.consumers
from Terminal import consumers

from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/channels/(?P<room_name>\w+)/$',
            consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/channels/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/webssh/', consumers.WebSSH.as_asgi()),
    path('ws/session/<int:id>', Core.consumers.Session.as_asgi()),
    re_path(r'ws/console/', Core.consumers.Console.as_asgi()),
    re_path(r'ws/message/', Core.consumers.ChatConsumer.as_asgi()),
]