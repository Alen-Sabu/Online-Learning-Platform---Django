"""
ASGI config for online_learning project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import assignments.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_learning.settings')

"""
ProtocalTypeRouter: This tells Django how to handle different types of connections
                    (HTTP and WebSocket)
AuthMiddlewareStack: This ensures that the WebSocket connections are authenticated
URLRouter: This routes WebSocket connections to the appropriate consumer based on the 
           URL patterns defined in 'routing.py'

"""
application = ProtocolTypeRouter({
    "http": get_asgi_application(), #handle traditional HTTP requests
    "websocket": AuthMiddlewareStack( #handle Websocket connections
        URLRouter(
            assignments.routing
        )
    )
})
get_asgi_application()
