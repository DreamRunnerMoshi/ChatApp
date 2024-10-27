# myapp/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from myproject.consumers import ChatGPTConsumer
from .chat_models import LangChainGPT

websocket_urlpatterns = [
    path('ws/chatgpt/', ChatGPTConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
