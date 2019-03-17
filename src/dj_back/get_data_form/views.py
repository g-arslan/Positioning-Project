import threading

from django.http import FileResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from get_data_form.data_process.file_process import FileProcessing
from get_data_form.models import Submission, Result, STATUS_CHOICES_TEXT
from .forms import SubmissionForm

import os

@login_required()
def submit_data(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Submission(
                user=request.user,
                sub_datetime=timezone.now(),
                data_file=request.FILES['data_file'],
                filename=os.path.basename(request.FILES['data_file'].name),
            )
            request.user.submissions_count += 1
            request.user.save()
            instance.save()
            result_instance = Result(
                submission=instance,
                status='P'
            )
            result_instance.save()
            threading.Thread(target=FileProcessing().process_file, args=(instance, result_instance)).start()
            # return render(request, 'get_data_form/submit_data.html', data)
            return redirect('submit_data')
    data = {'results': list(Result.objects.filter(submission__user=request.user).order_by('-submission__sub_datetime'))}
    for i in range(len(data['results'])):
        data['results'][i].status = STATUS_CHOICES_TEXT[data['results'][i].status]
        data['results'][i].result_csv = reverse('get_file') + '?res_id={res_id}'.format(res_id=data['results'][i].id)
    data['form'] = SubmissionForm()
    return render(request, 'get_data_form/submit_data.html', data)


@login_required()
def get_file(request):
    try:
        res_id = request.GET['res_id']
        result = Result.objects.filter(id=res_id).first()
        if result.submission.user == request.user:
            return FileResponse(result.result_csv, as_attachment=True)
    except:
        return redirect('submit_data')
