from rest_framework import status, views, viewsets
from rest_framework.decorators import action, api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import AssessmentScenario, Question, RecordingStep, ResponseData, Assessment, PatientFile
from accounts.models import User
from .serializers import (
    AssessmentSerializer,
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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import analyze_autism_traits_with_gemini


class AssessmentScenarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssessmentScenario.objects.all()
    serializer_class = AssessmentScenarioSerializer

class AssessmentCreateView(views.APIView):
    def post(self, request):
        # Extract assessment creation input from request data
        input_data = {
            "assessment_date": request.data.get("assessment_date", ""),
            "result_summary": request.data.get("result_summary", ""),
            "additional_notes": request.data.get("additional_notes", ""),
            "as_id": request.data.get("as_id"),
            "patient_id": request.data.get("patient_id"),
        }

        
        # Validate required fields
        if not input_data["as_id"] or not input_data["patient_id"]:
            return Response({'status': 'error', 'message': 'Missing as_id or patient_id.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Assessment instance
        try:
            scenario = get_object_or_404(AssessmentScenario, pk=input_data["as_id"])
            user = get_object_or_404(User, pk=input_data["patient_id"])
            assessment = Assessment.objects.create(
                assessment_date=input_data["assessment_date"],
                result_summary=input_data["result_summary"] or "",
                additional_notes=input_data["additional_notes"] or "",
                as_id=scenario,
                patient_id=user,
            )
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'success', 'assessment_id': assessment.id}, status=status.HTTP_201_CREATED)

class AssessmentDataViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssessmentSerializer

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id')
        queryset = Assessment.objects.all()
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
    

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
        answers = request.data.get('answers', [])
        if not isinstance(answers, list) or not answers:
            return Response({'status': 'error', 'message': 'Missing or invalid answers list.'}, status=status.HTTP_400_BAD_REQUEST)

        created_ids = []
        for answer in answers:
            question_id = answer.get('question_id')
            assessment_id = answer.get('assessment_id')
            response_text = answer.get('response_text', '')
            print(assessment_id,question_id)
            if not question_id or not assessment_id:
                continue  # Skip invalid entries

            question = get_object_or_404(Question, pk=question_id)
            assessment = get_object_or_404(Assessment, pk=assessment_id)

            print(question,assessment)
            response = ResponseData.objects.create(
                question_id=question,
                assessment_id=assessment,
                response_text=response_text,
            )
            created_ids.append(response.id)

        if not created_ids:
            return Response({'status': 'error', 'message': 'No valid answers provided.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'success', 'ids': created_ids}, status=status.HTTP_201_CREATED)
    
class ResponseDataViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResponseDataSerializer

    def get_queryset(self):
        assessment_id = self.kwargs.get('assessment_id')
        question_id = self.request.query_params.get('question_id')
        queryset = ResponseData.objects.all()
        if assessment_id:
            queryset = queryset.filter(assessment_id=assessment_id)
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        return queryset
    




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

class ReportCreateView(views.APIView):
    # If you need to disable CSRF, it's usually handled by DRF's authentication/permission classes
    # or globally in settings.py for API use cases.
    # For a public API endpoint, you might explicitly disable it via:
    # authentication_classes = []
    # permission_classes = []
    # But generally, don't use @csrf_exempt on a DRF APIView method.

    def post(self, request, *args, **kwargs): # Use 'post' method for POST requests
        try:
            user_answers = request.data.get('user_answers', {})
            assessment_id = request.data.get('assessment_id')

            # When using DRF's APIView, request.data already handles JSON parsing
            # So, you don't need json.loads(request.body)
            # data = request.data
            
            # Since you're hardcoding, we'll keep that for now for testing
            # In production, uncomment request.data and remove the hardcoded part.
            # user_answers = data.get('user_answers') # When getting from request.data

            user_answers = {
                # Factual/Concrete Questions
                "What is the color of a fire truck?": "Red",
                "How many legs does a spider have?": "Eight",
                "What is the shape of a soccer ball?": "Sphere",
                "What sound does a cat make?": "Meow",
                "What do you use to write on paper?": "Pencil",
                "What is frozen water called?": "Ice",
                "What planet do humans live on?": "Earth",
                "How many hours are in one day?": "24",
                "What is the opposite of 'day'?": "Night",
                "What comes after the number 5?": "6",

                # Safety/Routine Questions
                "What should you do before crossing the street?": "Look both ways",
                "Where do you go when there's a fire?": "Exit",
                "What do you wear when it's raining?": "Raincoat",
                "How often should you brush your teeth?": "Twice daily",
                "What do you do when lights turn red?": "Stop",

                # Sensory/Objects Questions
                "What texture is sandpaper?": "Rough",
                "What is the taste of lemon?": "Sour",
                "What instrument has black and white keys?": "Piano",
                "What animal has black and white stripes?": "Zebra",
                "Where do you find refrigerator?": "Kitchen",

                # Nature/Science Questions
                "What plant grows from acorn?": "Oak tree",
                "What is the largest ocean?": "Pacific",
                "What gas do humans breathe?": "Oxygen",
                "What season comes after winter?": "Spring",
                "What melts in sunshine?": "Snow",

                # Time/Dates Questions
                "How many days in one week?": "7",
                "What month comes after April?": "May",
                "What holiday is on December 25?": "Christmas",
                "What meal comes after lunch?": "Dinner",
                "When does sunrise happen?": "Morning",

                # Food Questions
                "What fruit is yellow and curved?": "Banana",
                "What do you pour on cereal?": "Milk",
                "Where does honey come from?": "Bees",
                "What vegetable makes you cry?": "Onion",
                "What is frozen dessert?": "Ice cream",

                # Body/Health Questions
                "How many fingers on one hand?": "5",
                "Where is your elbow?": "Arm",
                "What helps you see?": "Eyes",
                "What exercise makes heart beat faster?": "Running",
                "What do bandages protect?": "Cuts",

                # Transportation Questions
                "What vehicle flies in sky?": "Airplane",
                "What has two wheels?": "Bicycle",
                "Where do trains run?": "Tracks",
                "What color is school bus?": "Yellow",
                "What moves boats?": "Motor",

                # Home Questions
                "Where do you sleep?": "Bed",
                "What keeps room bright?": "Light",
                "What appliance cooks food?": "Stove",
                "Where do clothes go?": "Closet",
                "What cleans dishes?": "Dishwasher",

                # Animals Questions
                "What bird says 'hoot'?": "Owl",
                "What sea animal has tentacles?": "Octopus",
                "What farm animal gives milk?": "Cow",
                "What insect makes web?": "Spider",
                "What is fastest land animal?": "Cheetah"
            }
            
            if user_answers:
                analysis_result = analyze_autism_traits_with_gemini(user_answers)
                updated = Assessment.objects.filter(id=assessment_id).update(result_summary=analysis_result)
                if updated == 0:
                    return Response({'error': f'Assessment with id {assessment_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                # Use DRF's Response object for API responses
                return Response({'analysis': analysis_result}, status=status.HTTP_200_OK)
            return Response({'error': 'No user answers provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: # Catch a broader exception for debugging
            # For debugging, print the error
            print(f"Error in ReportCreateView: {e}")
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)