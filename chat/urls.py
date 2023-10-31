from django.urls import path
from . import views


urlpatterns = [
    # Chat rooms URLs
    path('chat-rooms/', views.ChatRoomListCreateView.as_view(), name='chat-room-list'),
    path('chat-rooms/<int:pk>/', views.ChatRoomDetailView.as_view(), name='chat-room-detail'),

    # Messages URLs
    path('messages/', views.MessageListCreateView.as_view(), name='message-list'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),

    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
