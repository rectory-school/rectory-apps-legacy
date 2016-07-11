# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def forwards(apps, schema_editor):
    AcademicYear = apps.get_model("academics", "AcademicYear")
    Enrollment = apps.get_model("academics", "Enrollment")
    
    Evaluable = apps.get_model("courseevaluations", "Evaluable")
    
    if Evaluable.objects.all().count() > 0:
        academic_year = AcademicYear.objects.get(current=True)
    
        for evaluable in Evaluable.objects.all():
            enrollment = Enrollment.objects.get(student=evaluable.student, academic_year=academic_year)
            evaluable.enrollment = enrollment
            evaluable.save()

def backwards(apps, schema_editor):
    Evaluable = apps.get_model("courseevaluations", "Evaluable")
    
    Evaluable.objects.update(enrollment=None)
    

class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0017_evaluable_enrollment'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
