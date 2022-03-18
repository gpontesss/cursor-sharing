import os

import django
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from config.urls import wspatterns

application = ProtocolTypeRouter(
    {"http": get_asgi_application(), "websocket": wspatterns}
)
