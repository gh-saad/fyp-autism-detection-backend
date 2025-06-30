# authentication/services/email_service.py

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_otp_email(email, otp_code):
    """Sends an OTP to the user's email."""
    subject = 'Your OTP for Autism App Registration'
    html_message = render_to_string('email/otp_email.html', {'otp_code': otp_code})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'no-reply@autismapp.com'
    recipient_list = [email]
    try:
        sent_count = send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        if sent_count > 0:
            print(f"OTP email successfully sent to {email} (printed to console).")
            return True
        else:
            print(f"OTP email to {email} was not sent (0 emails sent). Check EMAIL_BACKEND configuration.")
            return False
    except Exception as e:
        print(f"Error sending OTP email to {email}: {e}")
        return False

def send_password_reset_email(email, reset_link):
    """Sends a password reset link to the user's email."""
    subject = 'Password Reset Request for Autism App'
    html_message = render_to_string('email/password_reset_email.html', {'reset_link': reset_link})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'no-reply@autismapp.com'
    recipient_list = [email]
    try:
        sent_count = send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        if sent_count > 0:
            print(f"Password reset email successfully sent to {email} (printed to console).")
            return True
        else:
            print(f"Password reset email to {email} was not sent (0 emails sent). Check EMAIL_BACKEND configuration.")
            return False
    except Exception as e:
        print(f"Error sending password reset email to {email}: {e}")
        return False