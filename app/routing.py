# app/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/process/$', consumers.ProcessStreamConsumer.as_asgi()),
    re_path(r'ws/monitor/(?P<hostname>[^/]+)/$', consumers.ProcessBroadcastConsumer.as_asgi()),  # to UI

]
