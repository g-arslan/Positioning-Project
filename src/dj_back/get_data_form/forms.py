from django import forms
from django.forms import FileInput

from .models import Submission, Antenna


class SubmissionForm(forms.ModelForm):
    antenna = forms.ModelChoiceField(Antenna.objects)
    class Meta:
        model = Submission
        fields = ['data_file']
        labels = {
            'data_file': 'Your file'
        }


class AntennasForm(forms.Form):
    antennas = forms.FileField()
