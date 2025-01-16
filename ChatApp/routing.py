from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/room/<str:userid>/", consumers.MyConsumer.as_asgi(), name = 'websocketurl'),
]