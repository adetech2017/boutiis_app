from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegistrationView, ForgetPasswordView, ResetPasswordView, CustomTokenObtainPairView, UserDetailView, CurrentUserAPIView, UserListView
from . import views


urlpatterns = [
    # Other URL patterns
    path('get-csrf-token/', views.get_csrf_token, name='get-csrf-token'),
    # Token authentication views
    #path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # User registration, forget password, and reset password views
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/forget-password/', ForgetPasswordView.as_view(), name='forget-password'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    path('user/profile', CurrentUserAPIView.as_view(), name='user-profile'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='vendor-detail'),

    path('user/all-users', UserListView.as_view(), name='user-list'),

    #path('user/user-messages/', UserMessagesAPIView.as_view(), name='user-messages-api'),
    
]
