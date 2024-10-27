# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from myproject.chat_models.LangChainGPT import LangChainGPT

from .consumers import ChatGPTConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')


websocket_urlpatterns = [
    path('ws/chatgpt/', LangChainGPT.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
