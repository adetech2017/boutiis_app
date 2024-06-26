from rest_framework import serializers

from core.serializers import CustomUserSerializer
from .models import LiveForum



class ForumSerializer(serializers.ModelSerializer):
    interested_users = CustomUserSerializer(many=True)

    class Meta:
        model = LiveForum
        #fields = '__all__'
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'image', 'created_at', 'interested_users']
