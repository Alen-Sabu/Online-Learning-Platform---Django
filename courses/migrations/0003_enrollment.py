# Generated by Django 5.0.4 on 2024-05-16 17:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_rename_instructor_course_instructor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
    ]