from django.db import models
from core.models import User



class LiveForum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    interested_users = models.ManyToManyField(User, related_name='interested_forums')
    image = models.FileField(upload_to='forum_upload/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
