from django.urls import re_path
from . import consumers

"""
re_path - Define the urlpattern for websocket connections
NotificationConsumer - associate the url pattern which handles websocket connections
"""

websocket_urlpatterns = [
    re_path(r'ws/notification/$', consumers.NotificationConsumer.as_asgi()),
]