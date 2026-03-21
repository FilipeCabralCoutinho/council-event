from django import forms
from .models import Enrollment


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'name',
            'cpf',
            'church',
            'celphone',
            'emergency_contact',
            'email',
            'consent_given'
            ]
