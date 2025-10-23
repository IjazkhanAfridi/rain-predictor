from django.contrib import admin
from .models import PredictionRequest

@admin.register(PredictionRequest)
class PredictionRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'date', 'prediction_result', 'created_at']
    list_filter = ['created_at', 'prediction_result']
    search_fields = ['user__email', 'location']
    ordering = ['-created_at']
