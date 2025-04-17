from django.contrib import admin
from courses.models import Instructor, Course, Lecture, Enrollment, Category, LectureProgress

# Register your models here.

admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Enrollment)
admin.site.register(Category)
admin.site.register(LectureProgress)