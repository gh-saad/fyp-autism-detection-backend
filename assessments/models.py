from django.db import models
from accounts.models import User


class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    contant_info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"File {self.id} for Patient {self.patient_id}"
    
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE) # optional or use default 0 no parent
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=50)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"File {self.id} for Patient {self.patient_id}"
        
class AssessmentScenario(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    img_path = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    priority = models.CharField(max_length=255, default='100')    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Scenario {self.id} - {self.model_name} (Level: {self.level})"
    
class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    as_id = models.ForeignKey(AssessmentScenario, on_delete=models.CASCADE)
    # patient_id = models.ForeignKey('PatientProfile', on_delete=models.CASCADE)
    assessment_date = models.DateField()
    result_summary = models.TextField()
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Assessment {self.id}"

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    as_id = models.ForeignKey(AssessmentScenario, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_order = models.CharField(max_length=255, default='100')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question {self.id} for Scenario {self.as_id.name}"
    
class ResponseData(models.Model):
    id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    assessment_id = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    response_text = models.TextField(blank=True, null=True)  # For text or descriptive answers
    model_name = models.CharField(max_length=255)
    model_response = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response {self.id} for Question {self.question.id} in Assessment {self.assessment.id}"
    
class RecordingStep(models.Model):
    id = models.AutoField(primary_key=True)
    as_id = models.ForeignKey(AssessmentScenario, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    img_path = models.CharField(max_length=255)
    expected_duration = models.DurationField()  # Duration of the step
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recording Step {self.step_number} for Scenario {self.assessment_scenario.name}"


class PatientFile(models.Model):
    id = models.AutoField(primary_key=True)
    assessment_id = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    step_id = models.ForeignKey(RecordingStep, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, choices=[('image', 'Image'), ('video', 'Video'), ('document', 'Document')])
    duration = models.DurationField()
    model_name = models.CharField(max_length=255)
    model_response = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"File {self.id} for Patient {self.patient_id}"