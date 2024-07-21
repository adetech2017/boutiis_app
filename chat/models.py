from django.db import models
from core.models import User




class PrivateRoom(models.Model):
    user1 = models.ForeignKey(User, related_name='user1_rooms', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2_rooms', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user1', 'user2')


class Message(models.Model):
    room = models.ForeignKey(PrivateRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'


class FileModel(models.Model):
    room = models.ForeignKey(PrivateRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='messages/files/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: [File: {self.file_name}]'