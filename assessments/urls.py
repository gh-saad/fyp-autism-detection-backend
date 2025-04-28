from django.urls import path
from . import views

urlpatterns = [
    path('scenarios/', views.get_all_assessment_scenarios, name='example'),
    path('questions/<int:assessment_id>/', views.get_assessment_questions, name='example'),
]    