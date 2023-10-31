from rest_framework import serializers
from .models import CustomUser
from rest_framework import status
from rest_framework import serializers, status



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'first_name', 'last_name', 'phone_number', 'occupation')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data.get('first_name', '')  # Optional field
        last_name = validated_data.get('last_name', '')    # Optional field
        phone_number = validated_data.get('phone_number', '')  # Optional field
        occupation = validated_data.get('occupation', '')  # Optional field
        
        # You can add your user creation logic here
        user = CustomUser.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number, occupation=occupation)

        if user:
            response_data = {
                'message': "User created successfully.",
                'statusCode': status.HTTP_201_CREATED,
                'user_id': user.id,  # Include any additional data you want to return
            }
            return response_data

        response_data = {
            'message': "Failed to create user.",
            'statusCode': status.HTTP_400_BAD_REQUEST,
        }
        return response_data



class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)
