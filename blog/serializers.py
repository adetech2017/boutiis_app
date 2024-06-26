from rest_framework import serializers

from core.serializers import CustomUserSerializer
from .models import BlogPost, Forum, ForumTopic, ForumComment, Comment, Like






class ForumCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumComment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    post_likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'
    
    # Add the 'image' field for file uploads
    image = serializers.FileField(required=False)

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        blog_post = BlogPost.objects.create(**validated_data)

        # Handle the image file if it exists
        if image:
            blog_post.image = image
            blog_post.save()

        return blog_post





class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'


class ForumTopicSerializer(serializers.ModelSerializer):
    comments = ForumCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = ForumTopic
        fields = '__all__'

    # The 'image' field should be part of the serializer
    image = serializers.FileField(required=False)

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        forum_topic = ForumTopic.objects.create(**validated_data)

        # Handle the image file if it exists
        if image:
            forum_topic.image = image
            forum_topic.save()

        return forum_topic



