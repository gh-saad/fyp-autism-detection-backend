from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static
from .models import (
    Parent, Patient, AssessmentScenario, Assessment,
    Question, ResponseData, RecordingStep, PatientFile
)

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'contant_info', 'created_at', 'updated_at')
    search_fields = ('user_id__username', 'contant_info')
    list_filter = ('created_at',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'parent_id', 'name', 'date_of_birth', 'gender', 'created_at')
    search_fields = ('name', 'user_id__username')
    list_filter = ('gender', 'created_at')

@admin.register(AssessmentScenario)
class AssessmentScenarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_preview', 'name', 'level', 'model_name', 'priority', 'created_at')
    search_fields = ('name', 'model_name')
    list_filter = ('level', 'created_at')
    readonly_fields = ('img_preview',)

    def img_preview(self, obj):
        if obj.img_path:
            return format_html('<img src="{}" style="height: 50px;"/>', static(str(obj.img_path)))
        return "-"
    img_preview.short_description = 'Image'

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'as_id', 'assessment_date')
    search_fields = ('as_id__name',)
    list_filter = ('assessment_date',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'as_id', 'question_text', 'question_order', 'created_at')
    search_fields = ('question_text', 'as_id__name')
    list_filter = ('created_at',)

@admin.register(ResponseData)
class ResponseDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'assessment_id', 'model_name', 'model_response', 'created_at')
    search_fields = ('model_name', 'model_response')
    list_filter = ('created_at',)

@admin.register(RecordingStep)
class RecordingStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'as_id', 'number', 'name', 'expected_duration', 'created_at')
    search_fields = ('name', 'as_id__name')
    list_filter = ('created_at',)

@admin.register(PatientFile)
class PatientFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'assessment_id', 'step_id', 'file_type', 'model_name', 'created_at')
    search_fields = ('file_path', 'model_name')
    list_filter = ('file_type', 'created_at')