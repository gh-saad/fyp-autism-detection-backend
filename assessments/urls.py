from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssessmentDataViewSet,
    AssessmentScenarioViewSet,
    QuestionViewSet,
    RecordingStepViewSet,
    ResponseDataCreateView,
    PatientFileUploadView,
    AssessmentCreateView,
    ResponseDataViewSet,
    ReportCreateView
)

router = DefaultRouter()
router.register(r'scenarios', AssessmentScenarioViewSet, basename='scenario')

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:assessment_id>/', QuestionViewSet.as_view({'get': 'list'}), name='questions-by-assessment'),
    path('recording-steps/<int:assessment_id>/', RecordingStepViewSet.as_view({'get': 'list'}), name='steps-by-assessment'),
    path('answer/create', ResponseDataCreateView.as_view(), name='create-response'),
    path('patient-file/upload/', PatientFileUploadView.as_view(), name='upload-file'),
    path('create/', AssessmentCreateView.as_view(), name='create-assessment'),

    # path('assessment/', ResponseDataViewSet.as_view({'get': 'list'}), name='assessment'),
    path('assessment/', AssessmentDataViewSet.as_view({'get': 'list'}), name='assessment'),

    path('analyze-autism/', ReportCreateView.as_view(), name='analyze-autism'),
] 