from django.contrib import admin
from .models import AssessmentScenario

# Register your models here.
@admin.register(AssessmentScenario)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)