from django import forms
from django.forms import FileInput, Select

from .models import Submission, Antenna


class SubmissionForm(forms.ModelForm):
    antenna = forms.ModelChoiceField(Antenna.objects)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['antenna'].widget.attrs.update({'class': 'w3-select'})
        self.fields['data_file'].widget.attrs.update({'class': 'w3-input w3-button'})

    class Meta:
        model = Submission
        fields = ['data_file', 'antenna']
        labels = {
            'data_file': 'Your file'
        }


class AntennasForm(forms.Form):
    antennas = forms.FileField()
