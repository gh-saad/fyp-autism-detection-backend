from django.shortcuts import render
from django.http import JsonResponse
from .models import AssessmentScenario, Question

# Create your views here.
def get_all_assessment_scenarios(request):
    assessments = AssessmentScenario.objects.all().values()
    return JsonResponse(list(assessments), safe=False)


def get_assessment_questions(request, assessment_id):
    questions = Question.objects.filter(as_id=assessment_id).values()
    return JsonResponse(list(questions), safe=False)