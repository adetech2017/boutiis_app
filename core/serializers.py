from rest_framework import serializers, exceptions
from .models import User
from rest_framework import status
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from django.contrib.auth import authenticate
import random
from django.core.mail import send_mail
from django.dispatch import Signal
from rest_framework_simplejwt.tokens import RefreshToken



token_obtain_pair_created = Signal()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'date_of_birth', 'occupation', 'bio', 'profile_picture', 'is_online', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.occupation = validated_data.get('occupation', instance.occupation)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.is_online = validated_data.get('is_online', instance.is_online)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, TokenObtainSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            'password': attrs['password'],
        }
        identifier = attrs[self.username_field]
        
        # authenticate_kwargs = {
        #     self.username_field: attrs[self.username_field],
        #     'password': attrs['password'],
        # }
        
        # try:
        #     authenticate_kwargs['request'] = self.context['request']
        # except KeyError:
        #     pass

        try:
            #user = User.objects.get(email=authenticate_kwargs['email'])
            user = None
            if User.objects.filter(username=identifier).exists():
                user = User.objects.get(username=identifier)
            elif User.objects.filter(email=identifier).exists():
                user = User.objects.get(email=identifier)
            elif User.objects.filter(phone_number=identifier).exists():
                user = User.objects.get(phone_number=identifier)
            
            if user and not user.is_active:
                self.error_messages['no_active_account'] = {
                    'statusCode': 403,
                    'message': 'The account is inactive'
                }
                raise exceptions.AuthenticationFailed(
                    self.error_messages['no_active_account'],
                    'no_active_account',
                )
            elif not user:
                self.error_messages['no_active_account'] = {
                    'statusCode': 404,
                    'message': 'Account does not exist'
                }
                raise exceptions.AuthenticationFailed(
                    self.error_messages['no_active_account'],
                    'no_active_account',
                )

            authenticate_kwargs[self.username_field] = identifier

        except User.DoesNotExist:
            self.error_messages['no_active_account'] = {
                'statusCode': 404,
                'message': 'Account does not exist'
            }
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        user = self.custom_authenticate(authenticate_kwargs)
        if user is None:
            self.error_messages['no_active_account'] = {
                'statusCode': 401,
                'message': 'Credentials did not match'
            }
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        # Call the parent validate method to get the token
        data = super().validate(attrs)

        # Update is_online status
        user.is_online = True
        user.save(update_fields=['is_online'])

        user = self.user
        # Include user-related data
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['phone_number'] = user.phone_number
        data['username'] = user.username
        data['email'] = user.email
        data['is_active'] = user.is_active
        data['is_online'] = user.is_online


        # Emit signal for token creation
        refresh = self.get_token(user)
        token_obtain_pair_created.send(sender=RefreshToken, instance=refresh, created=True)


        return data
    
    def custom_authenticate(self, authenticate_kwargs):
        # Implement your custom authentication logic here
        # For example, you can check against a custom user model
        # or other authentication methods.
        
        user = authenticate(**authenticate_kwargs)
        return user


class ForgetPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate_identifier(self, value):
        if not User.objects.filter(username=value).exists() and not User.objects.filter(email=value).exists() and not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with this identifier does not exist.")
        return value

    def create(self, validated_data):
        identifier = validated_data['identifier']
        user = None

        if User.objects.filter(username=identifier).exists():
            user = User.objects.get(username=identifier)
        elif User.objects.filter(email=identifier).exists():
            user = User.objects.get(email=identifier)
        elif User.objects.filter(phone_number=identifier).exists():
            user = User.objects.get(phone_number=identifier)

        if user:
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
            # Here, you'd send the OTP to the user's email or phone number
            self.send_otp_to_user(user, otp)

        return user

    def send_otp_to_user(self, user, otp):
        # Dummy function to send OTP via email or SMS
        if user.email:
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
        elif user.phone_number:
            # Integrate with an SMS gateway to send the OTP to phone number
            pass


class ResetPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('identifier')
        otp = data.get('otp')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("The two password fields didn't match.")

        user = None

        if User.objects.filter(username=identifier, otp=otp).exists():
            user = User.objects.get(username=identifier, otp=otp)
        elif User.objects.filter(email=identifier, otp=otp).exists():
            user = User.objects.get(email=identifier, otp=otp)
        elif User.objects.filter(phone_number=identifier, otp=otp).exists():
            user = User.objects.get(phone_number=identifier, otp=otp)
        
        if not user:
            raise serializers.ValidationError("Invalid identifier or OTP.")

        data['user'] = user
        return data

    def save(self, validated_data):
        user = validated_data['user']
        new_password = validated_data['new_password']
        user.set_password(new_password)
        user.otp = None  # Clear the OTP after successful reset
        user.save()
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email','phone_number','date_of_birth','occupation','bio','profile_picture','is_online')


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()