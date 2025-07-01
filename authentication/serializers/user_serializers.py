# authentication/serializers/user_serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.encoding import force_str
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from dj_rest_auth.registration.views import SocialLoginView # Not directly used here, but good to know for dj-rest-auth integration
from django.conf import settings
import requests

User = get_user_model() # This will now correctly reference 'accounts.User'

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom user fields to the response
        data['id'] = self.user.id
        data['name'] = self.user.username  # Or self.user.get_full_name() if needed
        # You can also add: data['email'] = self.user.email

        return data
class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

class GoogleLoginSerializer(serializers.Serializer):
    """
    Serializer for handling Google OAuth2 ID tokens.
    Requires django-allauth.
    """
    access_token = serializers.CharField(required=True, write_only=True)

    def validate_access_token(self, access_token):
        # Verify the access token with Google's API
        try:
            # We assume a client-side flow where the client gets the access token
            # and sends it to the backend.
            # Here we verify it using Google's tokeninfo endpoint.
            response = requests.get(f"https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={access_token}")
            response.raise_for_status() # Raise an exception for bad status codes
            data = response.json()

            # Ensure the token is for your client_id (optional but recommended)
            if data.get('aud') != settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']:
                raise serializers.ValidationError("Invalid Google client ID for this token.")

            # Get user info from token
            self.user_info = {
                'email': data.get('email'),
                'username': data.get('email').split('@')[0], # Use email prefix as username
                'first_name': data.get('given_name', ''),
                'last_name': data.get('family_name', ''),
                'id_token': access_token # Store the access_token for allauth processing
            }
            return access_token
        except requests.RequestException as e:
            raise serializers.ValidationError(f"Google token validation failed: {e}")
        except Exception as e:
            raise serializers.ValidationError(f"Error validating Google token: {e}")

    def create(self, validated_data):
        # This method is not strictly used for user creation here as allauth handles it.
        # But we prepare the necessary data for the social login process.
        return self.user_info
