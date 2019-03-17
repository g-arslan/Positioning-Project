from django.contrib import admin

from .models import Submission, Result, Antenna

# Register your models here.

admin.site.register(Submission)
admin.site.register(Result)
admin.site.register(Antenna)
