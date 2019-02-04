from django.db import models

from users.models import CustomUser

import os

# Create your models here.

def data_file_name(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('data_files', '{user_id}_{submission_num}.{ext}'.format(
        user_id=instance.user.id,
        submission_num=instance.user.submissions_count,
        ext=ext,
    ))

class Submission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    sub_datetime = models.DateTimeField()
    data_file = models.FileField(upload_to=data_file_name, verbose_name='File with data')

    class Meta:
        ordering = ['sub_datetime']

    def __str__(self):
        return '{user} at {datetime}'.format(user=str(self.user), datetime=self.sub_datetime)


class Result(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.DO_NOTHING)
    result_file = models.FileField()

    def __str__(self):
        return str(self.submission)
