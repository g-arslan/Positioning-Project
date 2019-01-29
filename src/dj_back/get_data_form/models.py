from django.db import models

from users.models import CustomUser

# Create your models here.

class Submission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    sub_datetime = models.DateTimeField()
    data_file = models.FileField(upload_to='data_files/%d.%m.%Y-%H.%M.%S', verbose_name='File with data')

    class Meta:
        ordering = ['sub_datetime']

    def __str__(self):
        return '{user} at {datetime}'.format(user=str(self.user), datetime=self.sub_datetime)


class Result(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.DO_NOTHING)
    # TODO: fields that lead to result
