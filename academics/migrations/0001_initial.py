# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('year', models.CharField(unique=True, max_length=9)),
                ('current', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('course_name', models.CharField(max_length=255)),
                ('course_name_short', models.CharField(max_length=255)),
                ('course_name_transcript', models.CharField(max_length=255)),
                ('division', models.CharField(max_length=2)),
                ('grade_level', models.CharField(blank=True, max_length=2)),
                ('department', models.CharField(max_length=255)),
                ('course_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Dorm',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('dorm', models.CharField(max_length=20)),
                ('area', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('boarder', models.BooleanField()),
                ('grade', models.CharField(max_length=2)),
                ('division', models.CharField(max_length=2)),
                ('section', models.CharField(blank=True, max_length=1)),
                ('academic_year', models.ForeignKey(to='academics.AcademicYear', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('csn', models.CharField(max_length=255)),
                ('academic_year', models.ForeignKey(to='academics.AcademicYear', on_delete=models.CASCADE)),
                ('course', models.ForeignKey(to='academics.Course', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('student_id', models.CharField(unique=True, max_length=7)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('nickname', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('current', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('teacher_id', models.CharField(max_length=4)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='teacher',
            field=models.ForeignKey(null=True, blank=True, to='academics.Teacher', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='advisor',
            field=models.ForeignKey(null=True, blank=True, to='academics.Teacher', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='dorm',
            field=models.ForeignKey(null=True, blank=True, to='academics.Dorm', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(to='academics.Student', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='dorm',
            name='heads',
            field=models.ManyToManyField(related_name='_heads_+', to='academics.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('student', 'academic_year')]),
        ),
    ]
