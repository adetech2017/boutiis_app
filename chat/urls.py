from django.urls import path
from .views import MessageView, PrivateRoomView






urlpatterns = [
    path('api/messages/', MessageView.as_view(), name='message-list-create'),
    path('api/private-rooms/', PrivateRoomView.as_view(), name='private-room-create'),
    # Add other paths as needed for your application
]
