# authentication/services/auth_service.py

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken
from .email_service import send_otp_email, send_password_reset_email
from authentication.models import OTP
from django.utils import timezone 
from datetime import timedelta

User = get_user_model() # This will now correctly reference 'accounts.User'

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        """Registers a new user and sends OTP."""
        if User.objects.filter(email=email).exists():
            return None, "Email already registered."
        if User.objects.filter(username=username).exists():
            return None, "Username already taken."

        # Create user as inactive initially, will activate after OTP verification
        # Use your custom User manager's create_user method
        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        return user, None

    @staticmethod
    def generate_and_send_otp(user_email):
        """Generates a new OTP and sends it to the specified email."""
        # Delete any existing unverified OTP for this email
        OTP.objects.filter(email=user_email, is_used=False, expires_at__gt=timezone.now()).delete()

        otp = OTP.objects.create(email=user_email)
        success = send_otp_email(user_email, otp.otp_code) # Capture the return value
        if success:
            print(f"AuthService: OTP generation and email sending initiated for {user_email}. Result: SUCCESS")
            return True, "OTP sent successfully."
        else:
            print(f"AuthService: OTP generation and email sending initiated for {user_email}. Result: FAILED")
            return False, "Failed to send OTP."

    @staticmethod
    def verify_otp(email, otp_code):
        """Verifies the provided OTP."""
        try:
            otp_obj = OTP.objects.get(email=email, otp_code=otp_code, is_used=False)
            if otp_obj.is_valid():
                otp_obj.is_used = True
                otp_obj.save()
                # Activate the user if they exist and match the email
                user = User.objects.filter(email=email).first()
                if user and not user.is_active:
                    user.is_active = True
                    user.save()
                    otp_obj.user = user # Link OTP to user after activation
                    otp_obj.save()
                return True, "OTP verified successfully."
            else:
                return False, "OTP is invalid or expired."
        except OTP.DoesNotExist:
            return False, "Invalid OTP."

    @staticmethod
    def request_password_reset(email, request):
        """Handles the password reset request process."""
        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            uid = urlsafe_base64_encode(str(user.pk).encode())
            token = token_generator.make_token(user)

            # Construct the reset link
            # In a real app, this should be your frontend's password reset page
            # For example: http://localhost:3000/reset-password/{uid}/{token}
            reset_link = f"{request.build_absolute_uri('/')}api/auth/password-reset-confirm/{uid}/{token}/"

            if send_password_reset_email(email, reset_link):
                return True, "Password reset link sent to your email."
            return False, "Failed to send password reset email."
        except User.DoesNotExist:
            return False, "User with this email does not exist."

    @staticmethod
    def set_new_password(uidb64, token, new_password):
        """Sets a new password after successful verification."""
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, DjangoUnicodeDecodeError):
            return False, "Invalid password reset link."

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return False, "Invalid or expired password reset link."

        user.set_password(new_password)
        user.save()
        return True, "Password reset successfully."

    @staticmethod
    def get_tokens_for_user(user):
        """Generates JWT tokens for a given user."""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
