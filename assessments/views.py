from rest_framework import status, views, viewsets
from rest_framework.decorators import action, api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import AssessmentScenario, Question, RecordingStep, ResponseData, Assessment, PatientFile
from .serializers import (
    AssessmentScenarioSerializer,
    QuestionSerializer,
    RecordingStepSerializer,
    ResponseDataSerializer,
    PatientFileSerializer
)
import os
import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cv2


class AssessmentScenarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssessmentScenario.objects.all()
    serializer_class = AssessmentScenarioSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        assessment_id = self.kwargs.get('assessment_id')
        return Question.objects.filter(as_id=assessment_id)


class RecordingStepViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecordingStepSerializer

    def get_queryset(self):
        assessment_id = self.kwargs.get('assessment_id')
        return RecordingStep.objects.filter(as_id=assessment_id)


class ResponseDataCreateView(views.APIView):
    def post(self, request):
        question_id = request.data.get('question_id')
        assessment_id = request.data.get('assessment_id')
        response_text = request.data.get('response_text', '')

        if not question_id or not assessment_id:
            return Response({'status': 'error', 'message': 'Missing question_id or assessment_id.'}, status=status.HTTP_400_BAD_REQUEST)

        question = get_object_or_404(Question, pk=question_id)
        assessment = get_object_or_404(Assessment, pk=assessment_id)

        response = ResponseData.objects.create(
            question_id=question,
            assessment_id=assessment,
            response_text=response_text,
        )

        return Response({'status': 'success', 'id': response.id}, status=status.HTTP_201_CREATED)


class PatientFileUploadView(views.APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        assessment_id = request.data.get('assessment_id')
        step_id = request.data.get('step_id')
        file = request.FILES.get('file')

        if not file or not assessment_id or not step_id:
            return Response({'status': 'error', 'message': 'Missing file, assessment_id, or step_id.'}, status=status.HTTP_400_BAD_REQUEST)

        assessment = get_object_or_404(Assessment, pk=assessment_id)
        step = get_object_or_404(RecordingStep, pk=step_id)

        # Save file
        upload_dir = 'patient_media'
        file_name = default_storage.get_available_name(os.path.join(upload_dir, file.name))
        full_path = default_storage.save(file_name, ContentFile(file.read()))

        # Determine video duration
        duration = datetime.timedelta(seconds=0)
        if file.content_type.startswith('video/'):
            try:
                temp_file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                cap = cv2.VideoCapture(temp_file_path)
                if cap.isOpened():
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    if fps > 0:
                        seconds = int(frame_count / fps)
                        duration = datetime.timedelta(seconds=seconds)
                cap.release()
            except Exception:
                duration = datetime.timedelta(seconds=0)

        pf = PatientFile.objects.create(
            assessment_id=assessment,
            step_id=step,
            file_path=full_path,
            file_type=file.content_type,
            duration=duration,
        )

        return Response({'status': 'success', 'file_path': full_path, 'duration': str(duration)}, status=status.HTTP_201_CREATED)
