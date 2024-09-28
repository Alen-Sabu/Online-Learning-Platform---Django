from django.contrib import admin
from .models import Assignment, Submission, Notification

# Register your models here.
admin.site.register(Assignment)
admin.site.register(Notification)
admin.site.register(Submission)