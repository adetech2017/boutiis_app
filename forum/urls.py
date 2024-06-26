from django.urls import path
from .views import LiveForumListAPIView, LiveForumDetailAPIView

#app_name = 'forum'



urlpatterns = [
    path('live/forums/', LiveForumListAPIView.as_view(), name='forum-list-api'),
    path('live/forum/<int:pk>/', LiveForumDetailAPIView.as_view(), name='forum-detail-api'),
    # Add more URL patterns as needed
]
