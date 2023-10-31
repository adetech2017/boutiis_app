from django.urls import path
from . import views



urlpatterns = [
    # BlogPost URLs
    path('blogposts/', views.BlogPostListCreateView.as_view(), name='blogpost-list-create'),
    path('blogposts/<int:pk>/', views.BlogPostDetailView.as_view(), name='blogpost-detail'),
    path('blogposts/<int:blog_post_id>/comments/', views.BlogPostCommentsListView.as_view(), name='blogpost-comments-list'),
    
    # Comment URLs
    path('comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),

    # Like URLs
    path('likes/', views.LikeListCreateView.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', views.LikeDetailView.as_view(), name='like-detail'),

    # Forum URLs
    path('forums/', views.ForumListCreateView.as_view(), name='forum-list-create'),
    path('forums/<int:pk>/', views.ForumDetailView.as_view(), name='forum-detail'),

    # ForumTopic URLs
    path('forumtopics/', views.ForumTopicListCreateView.as_view(), name='forumtopic-list-create'),
    path('forumtopics/<int:pk>/', views.ForumTopicDetailView.as_view(), name='forumtopic-detail'),

    # ForumComment URLs
    path('forumcomments/', views.ForumCommentListCreateView.as_view(), name='forumcomment-list-create'),
    path('forumcomments/<int:pk>/', views.ForumCommentDetailView.as_view(), name='forumcomment-detail'),
]
