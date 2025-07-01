from rest_framework import serializers
from .models import AssessmentScenario, Question, RecordingStep, ResponseData, PatientFile

class AssessmentScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentScenario
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class RecordingStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingStep
        fields = '__all__'


class ResponseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseData
        fields = '__all__'


class PatientFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientFile
        fields = '__all__'
