from rest_framework import serializers
from .models import Message, PrivateRoom
from django.contrib.auth.models import User
from core.serializers import UserSerializer
from rest_framework.exceptions import ValidationError





class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'timestamp']

class PrivateRoomSerializer(serializers.ModelSerializer):
    user1 = serializers.StringRelatedField(read_only=True)
    user2 = serializers.StringRelatedField(read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = PrivateRoom
        fields = ['id', 'user1', 'user2', 'messages']

    def create(self, validated_data):
        user1 = self.context['request'].user
        user2 = validated_data.get('user2')

        existing_room = PrivateRoom.objects.filter(user1=user1, user2=user2).first() or PrivateRoom.objects.filter(user1=user2, user2=user1).first()

        if existing_room:
            return existing_room

        room = PrivateRoom(user1=user1, user2=user2)
        room.save()
        return room

