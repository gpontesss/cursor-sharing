import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from config.urls import wspatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = ProtocolTypeRouter(
    {"http": get_asgi_application(), "websocket": wspatterns}
)
