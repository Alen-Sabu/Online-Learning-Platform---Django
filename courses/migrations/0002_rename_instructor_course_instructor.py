# Generated by Django 5.0.4 on 2024-05-15 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='Instructor',
            new_name='instructor',
        ),
    ]
