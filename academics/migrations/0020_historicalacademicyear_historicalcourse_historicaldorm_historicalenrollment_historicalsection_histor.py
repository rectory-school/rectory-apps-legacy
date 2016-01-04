# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import academics.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0019_enrollment_enrolled_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAcademicYear',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', auto_created=True, blank=True)),
                ('year', models.CharField(db_index=True, max_length=9)),
                ('current', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True)),
            ],
            options={
                'verbose_name': 'historical academic year',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCourse',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', auto_created=True, blank=True)),
                ('number', models.CharField(db_index=True, max_length=20)),
                ('course_name', models.CharField(max_length=255)),
                ('course_name_short', models.CharField(max_length=255)),
                ('course_name_transcript', models.CharField(max_length=255)),
                ('division', models.CharField(max_length=2)),
                ('grade_level', models.CharField(max_length=2, blank=True)),
                ('department', models.CharField(max_length=255)),
                ('course_type', models.CharField(max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True)),
            ],
            options={
                'verbose_name': 'historical course',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalDorm',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', auto_created=True, blank=True)),
                ('dorm_name', models.CharField(db_index=True, max_length=20)),
                ('building', models.CharField(max_length=20)),
                ('wing', models.CharField(max_length=20, blank=True)),
                ('level', models.CharField(max_length=20, blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True)),
            ],
            options={
                'verbose_name': 'historical dorm',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalEnrollment',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', auto_created=True, blank=True)),
                ('boarder', models.BooleanField()),
                ('grade', models.CharField(max_length=2)),
                ('division', models.CharField(max_length=2)),
                ('section', models.CharField(max_length=1, blank=True)),
                ('status_enrollment', models.CharField(max_length=20, blank=True)),
                ('status_attending', models.CharField(max_length=20, blank=True)),
                ('enrolled_date', models.DateField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('academic_year', models.ForeignKey(db_constraint=False, to='academics.AcademicYear', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', blank=True, null=True)),
                ('advisor', models.ForeignKey(db_constraint=False, to='academics.Teacher', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', blank=True, null=True)),
                ('dorm', models.ForeignKey(db_constraint=False, to='academics.Dorm', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', blank=True, null=True)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True)),
                ('student', models.ForeignKey(db_constraint=False, to='academics.Student', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'historical enrollment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSection',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', auto_created=True, blank=True)),
                ('csn', models.CharField(max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('academic_year', models.ForeignKey(db_constraint=False, to='academics.AcademicYear', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', blank=True, null=True)),
                ('course', models.ForeignKey(db_constraint=False, to='academics.Course', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', blank=True, null=True)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True)),
                ('teacher', models.ForeignKey(db_constraint=False, to='academics.Teacher', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'historical section',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStudent',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', auto_created=True, blank=True)),
                ('student_id', models.CharField(db_index=True, max_length=7)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=255, blank=True)),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('current', models.BooleanField(default=False)),
                ('auth_key', models.CharField(max_length=63, default=academics.models.default_auth_key)),
                ('rectory_password', models.CharField(max_length=254, blank=True)),
                ('username', models.CharField(max_length=254, blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True)),
            ],
            options={
                'verbose_name': 'historical student',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStudentRegistration',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', auto_created=True, blank=True)),
                ('student_reg_id', models.CharField(db_index=True, max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True)),
                ('section', models.ForeignKey(db_constraint=False, to='academics.Section', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', blank=True, null=True)),
                ('student', models.ForeignKey(db_constraint=False, to='academics.Student', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'historical student registration',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTeacher',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', auto_created=True, blank=True)),
                ('teacher_id', models.CharField(db_index=True, max_length=5)),
                ('unique_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('prefix', models.CharField(max_length=255, blank=True)),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True)),
            ],
            options={
                'verbose_name': 'historical teacher',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
    ]
