from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/room/<str:room_name>", consumers.MyConsumer.as_asgi()),
]