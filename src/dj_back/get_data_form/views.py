import threading

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from get_data_form.data_process.file_process import FileProcessing
from get_data_form.models import Submission
from .forms import SubmissionForm

@login_required()
def submit_data(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Submission(
                user=request.user,
                sub_datetime=timezone.now(),
                data_file=request.FILES['data_file']
            )
            request.user.submissions_count += 1
            request.user.save()
            instance.save()
            threading.Thread(target=FileProcessing().process_file, args={'submission': instance})
            return render(request, 'get_data_form/submit_success.html')
            # return redirect('submit_success')
    else:
        form = SubmissionForm()
    return render(request, 'get_data_form/submit_data.html', {'form': form})


@login_required()
def submit_success(request):
    return render(request, 'get_data_form/submit_success.html')
