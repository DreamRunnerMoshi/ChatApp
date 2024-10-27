"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.http import HttpResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

def index(request):
    return HttpResponse("Hello, world!")

urlpatterns = [
    path('', index),
]

application = get_wsgi_application()
