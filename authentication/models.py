# authentication/models.py

from django.db import models
from django.contrib.auth import get_user_model
import random
# Fix: Import timezone for timezone-aware datetimes
from django.utils import timezone 
from datetime import timedelta

User = get_user_model()

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True) # OTP linked to email, can be for unverified users
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.otp_code:
            self.otp_code = str(random.randint(100000, 999999))
        if not self.expires_at:
            # Fix: Use timezone.now() for timezone-aware datetime
            self.expires_at = timezone.now() + timedelta(minutes=5) # OTP valid for 5 minutes
        super().save(*args, **kwargs)

    def is_valid(self):
        # Fix: Use timezone.now() for comparison
        return not self.is_used and self.expires_at > timezone.now()

    def __str__(self):
        return f"OTP for {self.email}: {self.otp_code}"