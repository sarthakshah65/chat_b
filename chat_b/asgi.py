"""
ASGI config for chat_b project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from django.urls import path,re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import chat_consumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_b.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

ws_url_patterns=[
    re_path(r"ws/chat/(?P<room_name>\w+)/$", chat_consumer.as_asgi()),
]
application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": 
            URLRouter(ws_url_patterns)
        
    
})