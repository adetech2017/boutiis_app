from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, parsers
from .models import BlogPost, Comment, Like, Forum, ForumComment, ForumTopic
from .serializers import BlogPostSerializer, CommentSerializer, LikeSerializer, ForumSerializer, ForumTopicSerializer, ForumCommentSerializer




class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': "Blog post created successfully.",
                'statusCode': status.HTTP_201_CREATED,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'message': "Failed to create blog post.",
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            'message': "Blog post deleted successfully.",
            'statusCode': status.HTTP_204_NO_CONTENT,
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': "Comment created successfully.",
                'statusCode': status.HTTP_201_CREATED,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'message': "Failed to create comment.",
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            'message': "Comment deleted successfully.",
            'statusCode': status.HTTP_204_NO_CONTENT,
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': "Like created successfully.",
                'statusCode': status.HTTP_201_CREATED,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'message': "Failed to create like.",
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'errors': serializer.errors,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)




class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            'message': "Like deleted successfully.",
            'statusCode': status.HTTP_204_NO_CONTENT,
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class ForumListCreateView(generics.ListCreateAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': "Forum created successfully.",
                'statusCode': status.HTTP_201_CREATED,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'message': "Failed to create forum.",
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ForumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            'message': "Forum deleted successfully.",
            'statusCode': status.HTTP_204_NO_CONTENT,
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class ForumTopicListCreateView(generics.ListCreateAPIView):
    queryset = ForumTopic.objects.all()
    serializer_class = ForumTopicSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': "Forum topic created successfully.",
                'statusCode': status.HTTP_201_CREATED,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'message': "Failed to create forum topic.",
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ForumTopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ForumTopic.objects.all()
    serializer_class = ForumTopicSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            'message': "Forum topic deleted successfully.",
            'statusCode': status.HTTP_204_NO_CONTENT,
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class ForumCommentListCreateView(generics.ListCreateAPIView):
    queryset = ForumComment.objects.all()
    serializer_class = ForumCommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': "Forum comment created successfully.",
                'statusCode': status.HTTP_201_CREATED,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'message': "Failed to create forum comment.",
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ForumCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ForumComment.objects.all()
    serializer_class = ForumCommentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            'message': "Forum comment deleted successfully.",
            'statusCode': status.HTTP_204_NO_CONTENT,
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class BlogPostCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Get the blog_post_id from the URL parameter
        blog_post_id = self.kwargs['blog_post_id']
        
        # Fetch comments related to the specified blog post
        return Comment.objects.filter(post__id=blog_post_id)
