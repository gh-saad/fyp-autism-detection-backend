from rest_framework import serializers
from .models import Consultant, Slot, Appointments
from accounts.models import User
from assessments.models import Patient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ConsultantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Consultant
        fields = ['id', 'user', 'contact_info', 'experience', 'education', 'specialization', 'created_at', 'updated_at']


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = '__all__'
