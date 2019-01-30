from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    submissions_count = models.IntegerField(verbose_name='Submissions count', default=0)

    def __str__(self):
        return self.username
