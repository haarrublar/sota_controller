# chat/routing.py
from django.urls import path
from .consumers import ControllerConsumer

websocket_urlpatterns = [
    path('ws/controller-buttons/', ControllerConsumer.as_asgi()),
]