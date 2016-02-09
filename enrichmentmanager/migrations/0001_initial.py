# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnrichmentOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=254, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnrichmentSignup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('enrichment_option', models.ForeignKey(to='enrichmentmanager.EnrichmentOption')),
            ],
        ),
        migrations.CreateModel(
            name='EnrichmentSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalEnrichmentSlot',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', auto_created=True, db_index=True, blank=True)),
                ('date', models.DateField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical enrichment slot',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStudent',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', auto_created=True, db_index=True, blank=True)),
                ('student_id', models.CharField(max_length=8, db_index=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
            ],
            options={
                'verbose_name': 'historical student',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTeacher',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', auto_created=True, db_index=True, blank=True)),
                ('teacher_id', models.CharField(max_length=5, db_index=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical teacher',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('student_id', models.CharField(max_length=8, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('teacher_id', models.CharField(max_length=5, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='advisor',
            field=models.ForeignKey(to='enrichmentmanager.Teacher'),
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='advisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, related_name='+', null=True, to='enrichmentmanager.Teacher', blank=True),
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='history_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enrichmentsignup',
            name='slot',
            field=models.ForeignKey(to='enrichmentmanager.EnrichmentSlot'),
        ),
        migrations.AddField(
            model_name='enrichmentsignup',
            name='student',
            field=models.ForeignKey(to='enrichmentmanager.Student'),
        ),
        migrations.AddField(
            model_name='enrichmentoption',
            name='slot',
            field=models.ForeignKey(to='enrichmentmanager.EnrichmentSlot'),
        ),
        migrations.AddField(
            model_name='enrichmentoption',
            name='teacher',
            field=models.ForeignKey(to='enrichmentmanager.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='enrichmentsignup',
            unique_together=set([('slot', 'student')]),
        ),
        migrations.AlterUniqueTogether(
            name='enrichmentoption',
            unique_together=set([('slot', 'teacher')]),
        ),
    ]
