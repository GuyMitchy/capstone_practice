from django.db import models
from django.conf import settings

# Create your models here.

class Symptom(models.Model):
    SEVERITY_CHOICES = [
        (1, 'Very Mild'),
        (2, 'Mild'),
        (3, 'Moderate'),
        (4, 'Severe'),
        (5, 'Very Severe'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']