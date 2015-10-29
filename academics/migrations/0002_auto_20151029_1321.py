# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=9, unique=True)),
                ('current', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('course_name', models.CharField(max_length=255)),
                ('course_name_short', models.CharField(max_length=255)),
                ('course_name_transcript', models.CharField(max_length=255)),
                ('division', models.CharField(max_length=2)),
                ('grade_level', models.CharField(max_length=2, blank=True)),
                ('department', models.CharField(max_length=255)),
                ('course_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('boarder', models.BooleanField()),
                ('dorm', models.CharField(max_length=20, blank=True)),
                ('grade', models.CharField(max_length=2)),
                ('division', models.CharField(max_length=2)),
                ('section', models.CharField(max_length=1, blank=True)),
                ('academic_year', models.ForeignKey(to='academics.AcademicYear')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('csn', models.CharField(max_length=255)),
                ('academic_year', models.ForeignKey(to='academics.AcademicYear')),
                ('course', models.ForeignKey(to='academics.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('teacher_id', models.CharField(max_length=4)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='current',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='section',
            name='teacher',
            field=models.ForeignKey(blank=True, to='academics.Teacher', null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='advisor',
            field=models.ForeignKey(blank=True, to='academics.Teacher', null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(to='academics.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('student', 'academic_year')]),
        ),
    ]
