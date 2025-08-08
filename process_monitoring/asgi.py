import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'process_monitoring.settings')

# Setup Django before importing models or any model-dependent code
django.setup()

# Import AFTER django.setup()
from django.core.asgi import get_asgi_application
from app.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
