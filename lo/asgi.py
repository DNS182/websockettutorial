import os
from django.core.asgi import get_asgi_application
from channels.routing import URLRouter , ProtocolTypeRouter
import chat.routing



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lo.settings')

application = ProtocolTypeRouter({

    'http' : get_asgi_application(),
    'websocket' : URLRouter(
        chat.routing.websocket_urlpatterns
    )

})

