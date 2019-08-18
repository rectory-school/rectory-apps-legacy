# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0022_auto_20160203_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ethnicity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('ethnicity', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalEthnicity',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('ethnicity', models.CharField(max_length=200)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical ethnicity',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalMealTime',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('include_boarding_students', models.BooleanField(default=False)),
                ('include_day_students', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical meal time',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPinnedStudent',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical pinned student',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSeatFiller',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('seats', models.IntegerField()),
                ('display', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical seat filler',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTable',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('description', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical table',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTableAssignment',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('waitor', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical table assignment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='MealTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('include_boarding_students', models.BooleanField(default=False)),
                ('include_day_students', models.BooleanField(default=False)),
                ('include_grades', models.ManyToManyField(to='academics.Grade')),
            ],
        ),
        migrations.CreateModel(
            name='PinnedStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('meal_time', models.ForeignKey(to='seating_charts.MealTime', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='SeatFiller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('seats', models.IntegerField()),
                ('display', models.BooleanField(default=False)),
                ('meal_time', models.ManyToManyField(to='seating_charts.MealTime')),
            ],
        ),
        migrations.CreateModel(
            name='SeatingStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('enrollment', models.ForeignKey(to='academics.Enrollment', on_delete=models.CASCADE)),
                ('ethnicity', models.ForeignKey(null=True, to='seating_charts.Ethnicity', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
                ('for_meals', models.ManyToManyField(to='seating_charts.MealTime')),
            ],
        ),
        migrations.CreateModel(
            name='TableAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('waitor', models.BooleanField(default=False)),
                ('meal_time', models.ForeignKey(to='seating_charts.MealTime', on_delete=models.CASCADE)),
                ('student', models.ForeignKey(to='seating_charts.SeatingStudent', on_delete=models.CASCADE)),
                ('table', models.ForeignKey(to='seating_charts.Table', on_delete=models.CASCADE)),
            ],
            options={
                'permissions': (('view', 'Can view table assignments'), ('edit', 'Can edit table assignments')),
            },
        ),
        migrations.AddField(
            model_name='seatfiller',
            name='table',
            field=models.ForeignKey(to='seating_charts.Table', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='pinnedstudent',
            name='student',
            field=models.ForeignKey(to='seating_charts.SeatingStudent', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='pinnedstudent',
            name='table',
            field=models.ForeignKey(to='seating_charts.Table', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='layout',
            name='left_print',
            field=models.ForeignKey(related_name='+', to='seating_charts.MealTime', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='layout',
            name='right_print',
            field=models.ForeignKey(null=True, related_name='+', blank=True, to='seating_charts.MealTime', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='historicaltableassignment',
            name='meal_time',
            field=models.ForeignKey(null=True, db_constraint=False, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='seating_charts.MealTime'),
        ),
        migrations.AddField(
            model_name='historicaltableassignment',
            name='student',
            field=models.ForeignKey(null=True, db_constraint=False, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='seating_charts.SeatingStudent'),
        ),
        migrations.AddField(
            model_name='historicaltableassignment',
            name='table',
            field=models.ForeignKey(null=True, db_constraint=False, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='seating_charts.Table'),
        ),
        migrations.AddField(
            model_name='historicalseatfiller',
            name='table',
            field=models.ForeignKey(null=True, db_constraint=False, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='seating_charts.Table'),
        ),
        migrations.AddField(
            model_name='historicalpinnedstudent',
            name='meal_time',
            field=models.ForeignKey(null=True, db_constraint=False, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='seating_charts.MealTime'),
        ),
        migrations.AddField(
            model_name='historicalpinnedstudent',
            name='student',
            field=models.ForeignKey(null=True, db_constraint=False, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='seating_charts.SeatingStudent'),
        ),
        migrations.AddField(
            model_name='historicalpinnedstudent',
            name='table',
            field=models.ForeignKey(null=True, db_constraint=False, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='seating_charts.Table'),
        ),
        migrations.AlterUniqueTogether(
            name='tableassignment',
            unique_together=set([('meal_time', 'student')]),
        ),
        migrations.AlterUniqueTogether(
            name='pinnedstudent',
            unique_together=set([('student', 'meal_time')]),
        ),
    ]
