from django.test import TestCase
from .models import BlogPost, Comment, Forum, Like
from .serializers import BlogPostSerializer, CommentSerializer, ForumTopicSerializer
from core.models import User
from rest_framework.test import APITestCase
from django.urls import reverse


class BlogPostSerializerTest(TestCase):
    def test_valid_data(self):
        user = User.objects.create(username='testuser', password='password123')
        data = {
            'title': 'Test Blog Post',
            'content': 'This is a test blog post.',
            'author': user.id,
        }
        serializer = BlogPostSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            'title': 'Test Blog Post',
            'content': '',  # Invalid because content is required
        }
        serializer = BlogPostSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    # Add more test methods for serializer validation and data serialization

class CommentSerializerTest(TestCase):
    def test_valid_data(self):
        user = User.objects.create(username='testuser', password='password123')
        blog_post = BlogPost.objects.create(title='Test Blog Post', content='This is a test blog post.', author=user)
        data = {
            'post': blog_post.id,
            'author': user.id,
            'text': 'This is a valid comment.',
        }
        serializer = CommentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            'post': None,  # Invalid because 'post' is required
            'author': None,  # Invalid because 'author' is required
            'text': '',  # Invalid because 'text' is required
        }
        serializer = CommentSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class ForumTopicSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            'title': 'Test Forum Topic',
            'content': 'This is a test forum topic.',
            'author': self.user.id,
        }
        serializer = ForumTopicSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            'title': '',  # Invalid because 'title' is required
            'content': 'This is a test forum topic.',
            'author': None,  # Invalid because 'author' is required
        }
        serializer = ForumTopicSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class LikeViewsTest(APITestCase):
    def setUp(self):
        # Create a user for the like
        self.user = User.objects.create(username='testuser', password='password123')
        
        # Create a blog post that the like will be associated with
        self.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )

    def test_create_like(self):
        url = reverse('like-list-create')
        data = {
            'post': self.blog_post.id,  # Use the 'blog_post' attribute
            'user': self.user.id,  # Use the 'user' attribute
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)



class ForumTopicViewsTest(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create(username='testuser', password='password123')

    def test_create_forum_topic(self):
        url = reverse('forumtopic-list-create')
        data = {
            'title': 'New Forum Topic',
            'content': 'This is a new forum topic.',
            'author': self.user.id,  # Use the 'user' attribute
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password123')

        # Create a blog post
        self.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )

        # Create a like associated with the blog post
        self.like = Like.objects.create(post=self.blog_post, user=self.user)

    def test_like_creation(self):
        # Access the 'blog_post' attribute within the test
        self.assertEqual(self.like.post, self.blog_post)
        self.assertEqual(self.like.user, self.user)

    # Add more test methods for other model attributes and relationships

class ForumModelTest(TestCase):
    def setUp(self):
        self.forum = Forum.objects.create(title='Test Forum', description='This is a test forum.')

    def test_forum_creation(self):
        self.assertEqual(self.forum.title, 'Test Forum')
        self.assertEqual(self.forum.description, 'This is a test forum.')

    # Add more test methods for other model attributes and relationships
