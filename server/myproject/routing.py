# myapp/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from myproject.consumers import ChatGPTConsumer
from .chat_models import alchemist

websocket_urlpatterns = [
    path('ws/chatgpt/', ChatGPTConsumer.as_asgi()),
    path('ws/chat', alchemist.LangChainGPT.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
