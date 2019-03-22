from django import forms

from .models import Submission, Antenna


class SubmissionForm(forms.ModelForm):
    antenna = forms.ModelChoiceField(Antenna.objects)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['antenna'].widget.attrs.update({'class': 'w3-select'})
        self.fields['data_file'].widget.attrs.update({'class': 'w3-input w3-button'})
        self.fields['send_email_flag'].widget.attrs.update({'class': 'w3-check'})

    class Meta:
        model = Submission
        fields = ['data_file', 'antenna', 'send_email_flag']
        labels = {
            'data_file': 'Your file',
            'send_email_flag': 'Send me email with the results',
        }


class AntennasForm(forms.Form):
    antennas = forms.FileField()
