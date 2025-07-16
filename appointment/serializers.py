from rest_framework import serializers
from .models import Consultant, Slot, Appointments
from accounts.models import User

class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = '__all__'

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Add more fields as needed

class AppointmentSerializer(serializers.ModelSerializer):
    consultant_id = ConsultantSerializer(read_only=True)
    patient_id = UserSerializer(read_only=True)
    slot_id = SlotSerializer(read_only=True)

    class Meta:
        model = Appointments
        fields = '__all__'