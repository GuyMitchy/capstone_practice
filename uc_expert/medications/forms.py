from django import forms
from .models import Medication
from django.utils.html import format_html

class MedicationForm(forms.ModelForm):
    name = forms.ChoiceField(
        choices=Medication.MEDICATION_CHOICES,  # Use the grouped choices directly
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'medication-select'
        })
    )
    
    frequency = forms.ChoiceField(
        choices=Medication.FREQUENCY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'frequency-select'
        })
    )
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    dosage = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter dosage (e.g., 40mg)'
        })
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any additional notes about this medication'
        })
    )

    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'frequency', 'start_date', 'notes']