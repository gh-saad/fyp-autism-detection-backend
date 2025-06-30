# authentication/urls.py

from django.urls import path
from authentication.views import auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', auth_views.RegisterView.as_view(), name='register'),
    path('verify-otp/', auth_views.OTPVerifyView.as_view(), name='verify_otp'),
    path('resend-otp/', auth_views.ResendOTPView.as_view(), name='resend_otp'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # SimpleJWT default login
    path('login/custom/', auth_views.LoginView.as_view(), name='custom_login'), # Our custom login to check is_active
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', auth_views.ForgotPasswordRequestView.as_view(), name='forgot_password_request'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.SetNewPasswordView.as_view(), name='password_reset_confirm'),
    path('google-login/', auth_views.GoogleLoginView.as_view(), name='google_login'),
    # This is primarily for testing the allauth callback flow in development
    path('google-callback-test/', auth_views.google_auth_callback_test, name='google_callback_test'),
]

