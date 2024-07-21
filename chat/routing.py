from django.urls import re_path, path
from . import consumers




websocket_urlpatterns = [
    #re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<str:room_id>/', consumers.ChatConsumer.as_asgi()),
]
