from django.contrib import admin
from courses.models import Instructor, Course, Lecture, Enrollment
# Register your models here.

admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Enrollment)
