# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def migrade_grade_code_to_grade(app, schema_editor):
  Grade = app.get_model("academics", "Grade")
  Enrollment = app.get_model("academics", "Enrollment")
  
  grade_codes = Enrollment.objects.values_list('grade_code', flat=True).order_by().distinct()
  
  for grade_code in grade_codes:
    if not grade_code:
      continue
      
    grade = Grade()
    grade.grade = grade_code
    
    if grade_code == 'K':
      grade.description = 'Kindergarden'
    else:
      grade.description = 'Grade {grade_code:}'.format(grade_code = grade_code)
    
    grade.save()
    
    Enrollment.objects.filter(grade_code=grade_code).update(grade=grade)
    
class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0020_historicalacademicyear_historicalcourse_historicaldorm_historicalenrollment_historicalsection_histor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('grade', models.CharField(max_length=2, unique=True)),
                ('description', models.CharField(max_length=63, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='enrollment',
            old_name='grade',
            new_name='grade_code',
        ),
        migrations.RenameField(
            model_name='historicalenrollment',
            old_name='grade',
            new_name='grade_code',
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='grade_code',
            field=models.CharField(null=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='historicalenrollment',
            name='grade_code',
            field=models.CharField(null=True, max_length=2),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='grade',
            field=models.ForeignKey(null=True, to='academics.Grade'),
        ),
        migrations.AddField(
            model_name='historicalenrollment',
            name='grade',
            field=models.ForeignKey(blank=True, on_delete=models.deletion.DO_NOTHING, null=True, db_constraint=False, to='academics.Grade', related_name='+'),
        ),
        migrations.RunPython(
          migrade_grade_code_to_grade
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='grade_code',
        ),
        migrations.RemoveField(
            model_name='historicalenrollment',
            name='grade_code',
        ),
    ]
