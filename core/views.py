from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LogoutSerializer, UserSerializer, ForgetPasswordSerializer, ResetPasswordSerializer, CustomTokenObtainPairSerializer, CustomUserSerializer
from rest_framework.response import Response
from rest_framework import serializers, status, generics
from rest_framework.response import Response
from core.models import User
from django.db import IntegrityError
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken



def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                user_data = serializer.validated_data
                user = serializer.create(user_data)

                user_serializer = UserSerializer(user)

                response_data = {
                    'message': "User registered successfully.",
                    'statusCode': status.HTTP_201_CREATED,
                    'data': user_serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    'message': "Failed to register user. Please check the provided data.",
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'errors': serializer.errors,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Http404:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Unauthorized", "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                user = serializer.save()

                user_serializer = UserSerializer(user)

                response_data = {
                    'message': "User updated successfully.",
                    'statusCode': status.HTTP_200_OK,
                    'data': user_serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'message': "Failed to update user. Please check the provided data.",
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'errors': serializer.errors,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Http404:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Unauthorized", "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            # Check if the authentication was successful
            if response.status_code == status.HTTP_200_OK:
                data = response.data
                user_data = {
                    "refresh": data['refresh'],
                    "access": data['access'],
                    "first_name": data['first_name'],
                    "last_name": data['last_name'],
                    "phone_number": data['phone_number'],
                    "username": data['username'],
                    "email": data['email'],
                    "is_active": data['is_active'],
                    "is_online": data['is_online']
                }
                custom_response = {
                    "user_data": user_data,
                    "message": "Authentication successful",
                    "statusCode": status.HTTP_200_OK,
                }
                return Response(custom_response, status=status.HTTP_200_OK)
            elif response.status_code == status.HTTP_401_UNAUTHORIZED:
                custom_response = {
                    "message": "Authentication failed",
                    "statusCode": status.HTTP_401_UNAUTHORIZED,
                }
                return Response(custom_response, status=status.HTTP_401_UNAUTHORIZED)
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                custom_response = {
                    "message": "User not found",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                }
                return Response(custom_response, status=status.HTTP_404_NOT_FOUND)
            else:
                custom_response = {
                    "message": "Internal server error",
                    "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
                return Response(custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Http404:
            # Handle "404 Not Found" error
            custom_response = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'User not found'
            }
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)

class ForgetPasswordView(generics.CreateAPIView):
    serializer_class = ForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "detail": "OTP has been sent to the registered email or phone number."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Password has been reset successfully."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomHttp404(Http404):
    error_key = "user_not_found"

class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        try:
            user_instance = self.get_object()

            user_serializer = UserSerializer(user_instance)

            response_data = {
                "statusCode": status.HTTP_200_OK,
                "message": "user record retrieved successfully",
                "data": user_serializer.data,
                #"user": user_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Http404:
            # Handle the 404 error with a custom error message
            response_data = {
                "message": CustomHttp404.error_message,
                "errors": {
                    CustomHttp404.error_key: CustomHttp404.error_message
                }
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="update user record"
    )
    def update(self, request, *args, **kwargs):
        try:
            user_instance = self.get_object()
            
            user_serializer = UserSerializer(user_instance, data=request.data, partial=True)
            user_serializer.is_valid(raise_exception=True)  # Raise an exception for invalid data
            user_update_success = user_serializer.save()

            response_data = {
                "statusCode": status.HTTP_200_OK,
                "message": "User record updated successfully",
                "user": user_serializer.data,
                #"user": user_serializer.data,
            }

            if user_update_success:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # Return a 400 Bad Request status code if the user update was not successful
                return Response({"message": "User record not updated correctly"}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            response_data = {
                "message": "User not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class CurrentUserAPIView(generics.RetrieveAPIView):
    serializer_class =   CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the current logged-in user
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        try:
            # Retrieve the current user
            instance = self.get_object()

            if not instance:
                raise Http404("User not found")

            # Serialize the user data
            serializer = self.get_serializer(instance)
            data = serializer.data

            # Build the success response
            response_data = {
                "statusCode": status.HTTP_200_OK,
                "message": "User record retrieved successfully",
                "data": data,
            }

            # Return success response
            return Response(response_data, status=status.HTTP_200_OK)

        except Http404 as e:
            # Handle 404 - User not found
            response_data = {
                "statusCode": status.HTTP_404_NOT_FOUND,
                "message": str(e),
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle any other exception or error
            response_data = {
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Example: Include status and message in the response
        response_data = {
            'status': 'success',
            'message': 'Users retrieved successfully',
            'data': serializer.data,
        }

        return Response(response_data)



class LogoutView(generics.CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh_token']
        user = request.user

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Update the user's is_online status
            user.is_online = False
            user.save(update_fields=['is_online'])

            response_data = {
                'message': "User logged out successfully.",
                'statusCode': status.HTTP_200_OK
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                'message': "Logout failed.",
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



# class UserMessagesAPIView(generics.ListAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]


#     def get_queryset(self):
#         # Get users with whom the current user has messages
#         return User.objects.filter(
#             Q(sent_messages__receiver=self.request.user) | Q(received_messages__sender=self.request.user)
#         ).distinct()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)

#         # Enhance the response with additional details
#         user_data = []
#         for user in serializer.data:
#             user_id = self.get_user_id(user)  # Find the user ID dynamically

#             if user_id is not None:
#                 user_messages = Message.objects.filter(
#                     Q(sender=user_id, receiver=self.request.user) | Q(sender=self.request.user, receiver=user_id)
#                 ).order_by('-timestamp')[:5]

#                 message_data = MessageSerializer(user_messages, many=True).data

#                 user_data.append({
#                     **user,
#                     'recent_messages': message_data,
#                 })

#         return Response(user_data, status=status.HTTP_200_OK)

#     def get_user_id(self, user_data):
#         # Find the user ID dynamically from the serialized data
#         user_id_keys = ['id', 'pk']  # Possible keys representing user ID
#         for key in user_id_keys:
#             if key in user_data:
#                 return user_data[key]

#         # If no valid key is found, return None or a default value
#         return None