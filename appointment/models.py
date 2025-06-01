from django.db import models
from accounts.models import User
from assessments.models import Patient

# Create your models here.
class Consultant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultant_profile')
    contact_info = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    education = models.TextField()
    specialization = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.specialization})"
    
class Slot(models.Model):
    id = models.AutoField(primary_key=True)
    consultant_id = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    locatoin = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"File {self.id} for Patient {self.patient_id}"

class Appointments(models.Model):
    id = models.AutoField(primary_key=True)
    consultant_id = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"File {self.id} for Patient {self.patient_id}"