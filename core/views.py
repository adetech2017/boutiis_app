from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, ForgetPasswordSerializer, ResetPasswordSerializer
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string




class RegistrationView(TokenObtainPairView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # You can customize the response data as needed
            token = super().post(request, *args, **kwargs).data
            response_data = {
                'message': "User registered successfully.",
                'statusCode': status.HTTP_201_CREATED,
                'access_token': token['access'],
                'refresh_token': token['refresh'],
                'user_id': user.id,  # Include any additional data you want to return
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'message': "Failed to register user.",
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(CreateAPIView):
    serializer_class = ForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            form = PasswordResetForm({'email': email})
            if form.is_valid():
                form.save(request=request)

                user = form.user_cache

                # Send a password reset email
                current_site = get_current_site(request)
                subject = 'Password Reset'
                message = render_to_string(
                    'password_reset_email.html',
                    {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    }
                )
                from_email = 'your_email@example.com'  # Change to your email
                recipient_list = [user.email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            # Decode the UID and retrieve the user
            try:
                uid = urlsafe_base64_decode(uid).decode()
                user = get_user_model().objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
                user = None

            if user and default_token_generator.check_token(user, token):
                form = SetPasswordForm(user, {'new_password1': password, 'new_password2': password})
                if form.is_valid():
                    form.save()
                    return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Password reset failed.'}, status=status.HTTP_400_BAD_REQUEST)