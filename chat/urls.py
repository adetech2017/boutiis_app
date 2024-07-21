from django.urls import path
from .views import (PrivateRoomMessagesView,PrivateRoomView,UserChatsView,)






urlpatterns = [
    #path('api/messages/', MessageView.as_view(), name='message-list-create'),
    #path('api/private-rooms/', PrivateRoomView.as_view(), name='private-room-create'),
    # Add other paths as needed for your application
    #path('messages/', MessageView.as_view(), name='message'),
    #path('chat/rooms/', PrivateRoomView.as_view(), name='private_room'),
    path('chat/rooms/<int:user_id>/', PrivateRoomView.as_view(), name='private_room'),
    path('chat/rooms/<int:room_id>/messages/', PrivateRoomMessagesView.as_view(), name='room_messages'),
    path('user/chats/', UserChatsView.as_view(), name='user_chats'),
]
