from django.db import models
from django.contrib.auth.models import User


class PredictionRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    location = models.CharField(max_length=255)
    date = models.DateField()
    prediction_result = models.CharField(max_length=50)
    confidence = models.FloatField(null=True, blank=True)
    weather_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prediction Request'
        verbose_name_plural = 'Prediction Requests'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.location} - {self.date}"
