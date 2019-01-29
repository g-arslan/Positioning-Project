from django import forms
from django.forms import FileInput

from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['data_file']
        labels = {
            'data_file': 'Your file'
        }
