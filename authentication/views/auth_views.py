# authentication/views/auth_views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from authentication.serializers.user_serializers import (
    RegistrationSerializer,
    LoginSerializer,
    OTPVerificationSerializer,
    ForgotPasswordRequestSerializer,
    SetNewPasswordSerializer,
    GoogleLoginSerializer,
)
from authentication.services.auth_service import AuthService
from authentication.models import OTP

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp, SocialAccount
from allauth.socialaccount.signals import pre_social_login
from allauth.socialaccount.helpers import complete_social_login
from django.dispatch import receiver
from django.shortcuts import redirect
import json

User = get_user_model() # This will now correctly reference 'accounts.User'

# Handle custom authentication for social login if needed
class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def get_callback_url(self, request, app):
        # Ensure correct callback URL for local development or production
        if settings.DEBUG:
            # For local testing, ensure your redirect URI in Google Console is e.g., http://localhost:8000/accounts/google/login/callback/
            return "http://localhost:8000/accounts/google/login/callback/"
        return super().get_callback_url(request, app)


class RegisterView(generics.CreateAPIView):
    """
    Handles user registration.
    - Creates an inactive user.
    - Sends an OTP to the provided email.
    """
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user, error = AuthService.register_user(username, email, password)

        if error:
            return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)

        # Attempt to send OTP after user creation (even if user is inactive)
        success, message = AuthService.generate_and_send_otp(email)

        if not success:
            user.delete() # Rollback user creation if OTP sending fails
            return Response({'detail': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'User registered. Please verify your email with OTP.', 'email': email}, status=status.HTTP_201_CREATED)


class OTPVerifyView(generics.GenericAPIView):
    """
    Verifies the OTP sent to the user's email.
    - Activates the user if OTP is valid.
    """
    serializer_class = OTPVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']

        success, message = AuthService.verify_otp(email, otp_code)

        if success:
            user = User.objects.filter(email=email).first()
            if user:
                tokens = AuthService.get_tokens_for_user(user)
                return Response({'detail': message, 'tokens': tokens}, status=status.HTTP_200_OK)
            return Response({'detail': message + ' User not found after verification.'}, status=status.HTTP_200_OK)
        return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(generics.GenericAPIView):
    """
    Resends an OTP to the user's email.
    """
    serializer_class = ForgotPasswordRequestSerializer # Reusing serializer as it only needs email
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Check if user exists (if registering, they might not be active yet)
        if not User.objects.filter(email=email).exists() and not OTP.objects.filter(email=email, is_used=False).exists():
             return Response({'detail': 'No user or pending registration found for this email.'}, status=status.HTTP_404_NOT_FOUND)

        success, message = AuthService.generate_and_send_otp(email)

        if success:
            return Response({'detail': message}, status=status.HTTP_200_OK)
        return Response({'detail': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(TokenObtainPairView):
    """
    Handles user login and provides JWT tokens.
    - Requires active user (verified via OTP).
    """
    serializer_class = LoginSerializer # This will be handled by SimpleJWT's default serializer internally
    permission_classes = [AllowAny] # Allow unauthenticated users to access this

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            # If user is not active, prompt them to verify email
            return Response({
                'detail': 'Account not active. Please verify your email with OTP.',
                'email': email
            }, status=status.HTTP_403_FORBIDDEN)

        # Let SimpleJWT handle the actual authentication and token generation
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.data['id'] = user.id
            response.data['name'] = user.username  # or user.get_full_name() if you want full name

        return response


class ForgotPasswordRequestView(generics.GenericAPIView):
    """
    Handles the request for password reset.
    - Sends a password reset link to the user's email.
    """
    serializer_class = ForgotPasswordRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        success, message = AuthService.request_password_reset(email, request)

        if success:
            return Response({'detail': message}, status=status.HTTP_200_OK)
        return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordView(generics.GenericAPIView):
    """
    Sets a new password using the UID and Token from the reset link.
    """
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        success, message = AuthService.set_new_password(uidb64, token, new_password)

        if success:
            return Response({'detail': message}, status=status.HTTP_200_OK)
        return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginView(APIView):
    """
    Handles Google login by verifying the access token received from the client.
    Then, it uses django-allauth to create/login the user.
    """
    permission_classes = [AllowAny]
    serializer_class = GoogleLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data['access_token']

        # Use django-allauth's internal mechanisms to complete the social login
        # This requires setting up Google Social App in Django Admin
        try:
            adapter = CustomGoogleOAuth2Adapter(request)
            app = SocialApp.objects.get(provider='google', sites__id=settings.SITE_ID)
            adapter.client_class = OAuth2Client

            # This part simulates the call to allauth's complete_login
            # allauth typically expects an authorization code, but for mobile/JS clients,
            # we often get an access token. We need to manually construct a SocialLogin.

            # We need to get actual user data from google using the access token
            # The serializer's validate_access_token already fetches this and stores in self.user_info
            if not hasattr(serializer, 'user_info'):
                return Response({'detail': 'Failed to retrieve Google user info.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            sociallogin = adapter.complete_login(request, app, access_token=access_token)
            sociallogin.token = access_token
            sociallogin.state = 'authenticated' # A dummy state, as we're past the OAuth flow

            # This line processes the social login, creates/links user, etc.
            result = complete_social_login(request, sociallogin)

            # result will contain the authenticated user object or raise an exception
            user = result.user
            tokens = AuthService.get_tokens_for_user(user)

            return Response({
                'detail': 'Google login successful.',
                'tokens': tokens,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)

        except SocialApp.DoesNotExist:
            return Response({'detail': 'Google SocialApp not configured in Django Admin.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'detail': f'Google login failed: {e}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def google_auth_callback_test(request):
    """
    A dummy endpoint to test allauth's Google callback.
    This is for development/debugging how allauth redirects.
    """
    code = request.GET.get('code')
    error = request.GET.get('error')
    state = request.GET.get('state')
    return Response({
        'message': 'Google OAuth Callback received',
        'code': code,
        'error': error,
        'state': state
    }, status=status.HTTP_200_OK)
