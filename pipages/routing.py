from django.conf.urls import url
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.http import AsgiHandler


application = ProtocolTypeRouter({
    'http': URLRouter([
        url(r'', AsgiHandler)
    ])
})
