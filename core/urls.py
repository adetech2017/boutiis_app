from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegistrationView, ForgetPasswordView, ResetPasswordView



urlpatterns = [
    # Other URL patterns

    # Token authentication views
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # User registration, forget password, and reset password views
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/forget_password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('auth/reset_password/', ResetPasswordView.as_view(), name='reset_password'),
]
