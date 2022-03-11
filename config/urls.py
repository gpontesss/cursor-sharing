import cursor.views
from channels.routing import URLRouter
from cursor.consumers import CursorConsumer
from django.contrib import admin
from django.urls import path

urlpatterns = (
    path("admin/", admin.site.urls),
    path("cursor/", cursor.views.index),
)

wspatterns = URLRouter(
    (path("cursor/ws/", CursorConsumer.as_asgi()),),
)
