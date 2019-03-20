from django.db import models

from users.models import CustomUser

import os

# Create your models here.


class Antenna(models.Model):
    name = models.CharField(max_length=512, verbose_name='Antenna ID', unique=True, default='AUTO')

    def __str__(self):
        return str(self.name)


def data_file_name(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('data_files', '{user_id}_{submission_num}.{ext}'.format(
        user_id=instance.user.id,
        submission_num=instance.user.submissions_count,
        ext=ext,
    ))


class Submission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    antenna = models.CharField(max_length=512, verbose_name='Antenna ID', default='AUTO')
    sub_datetime = models.DateTimeField()
    data_file = models.FileField(upload_to=data_file_name, verbose_name='File with data')
    filename = models.CharField(max_length=256)

    class Meta:
        ordering = ['sub_datetime']

    def __str__(self):
        return '{user} at {datetime}'.format(user=str(self.user), datetime=self.sub_datetime)


class Result(models.Model):
    PROCESSING = 'P'
    UPLOADING = 'U'
    DONE = 'D'
    ERROR = 'E'
    STATUS_CHOICES = (
        (PROCESSING, 'Processing'),
        (UPLOADING, 'Uploading'),
        (DONE, 'Done'),
        (ERROR, 'Error')
    )
    STATUS_CHOICES_TEXT = dict(STATUS_CHOICES)

    submission = models.ForeignKey(Submission, on_delete=models.DO_NOTHING)
    result_csv = models.FileField(null=True)
    result_pdf = models.FileField(null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)

    def __str__(self):
        return str(self.submission) + ' ' + self.STATUS_CHOICES_TEXT[self.status]
