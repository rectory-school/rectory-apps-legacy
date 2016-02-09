# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0034_auto_20160204_1405'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSuppression',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('suppression_date', models.DateField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnrichmentOption',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=254)),
            ],
            options={
                'ordering': ['teacher__last_name', 'teacher__first_name'],
            },
        ),
        migrations.CreateModel(
            name='EnrichmentSignup',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('details', models.CharField(blank=True, max_length=255)),
                ('admin_lock', models.BooleanField(default=False)),
                ('enrichment_option', models.ForeignKey(to='enrichmentmanager.EnrichmentOption', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'permissions': (('can_view_own_advisees', 'Can view own advisees'), ('can_view_other_advisees', "Can view other advisor's advisees"), ('can_view_all_advisees', 'Can view the full advisee lists'), ('can_edit_own_advisees', 'Can edit own advisee signups'), ('can_edit_all_advisees', 'Can edit all advisees signups'), ('can_edit_same_day', 'Can edit advisee signups on the same day'), ('can_view_reports', 'Can view reports'), ('can_view_single_student', 'Can view single student'), ('can_override_admin_lock', 'Can override admin lock'), ('can_set_admin_lock', 'Can set admin lock')),
            },
        ),
        migrations.CreateModel(
            name='EnrichmentSlot',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('editable_until', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalEnrichmentOption',
            fields=[
                ('id', models.IntegerField(blank=True, auto_created=True, verbose_name='ID', db_index=True)),
                ('location', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=254)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
                ('slot', models.ForeignKey(null=True, blank=True, related_name='+', to='enrichmentmanager.EnrichmentSlot', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical enrichment option',
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalEnrichmentSignup',
            fields=[
                ('id', models.IntegerField(blank=True, auto_created=True, verbose_name='ID', db_index=True)),
                ('details', models.CharField(blank=True, max_length=255)),
                ('admin_lock', models.BooleanField(default=False)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('enrichment_option', models.ForeignKey(null=True, blank=True, related_name='+', to='enrichmentmanager.EnrichmentOption', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
                ('slot', models.ForeignKey(null=True, blank=True, related_name='+', to='enrichmentmanager.EnrichmentSlot', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical enrichment signup',
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalEnrichmentSlot',
            fields=[
                ('id', models.IntegerField(blank=True, auto_created=True, verbose_name='ID', db_index=True)),
                ('date', models.DateField(db_index=True)),
                ('editable_until', models.DateTimeField(null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical enrichment slot',
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStudent',
            fields=[
                ('id', models.IntegerField(blank=True, auto_created=True, verbose_name='ID', db_index=True)),
                ('lockout', models.CharField(blank=True, max_length=100)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical student',
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTeacher',
            fields=[
                ('id', models.IntegerField(blank=True, auto_created=True, verbose_name='ID', db_index=True)),
                ('default_room', models.CharField(blank=True, max_length=100)),
                ('default_description', models.CharField(blank=True, max_length=100)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical teacher',
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('lockout', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'ordering': ['student__last_name', 'student__first_name'],
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('default_room', models.CharField(blank=True, max_length=100)),
                ('default_description', models.CharField(blank=True, max_length=100)),
                ('teacher', models.ForeignKey(to='academics.Teacher')),
            ],
            options={
                'ordering': ['teacher__last_name', 'teacher__first_name'],
            },
        ),
        migrations.AddField(
            model_name='student',
            name='advisor',
            field=models.ForeignKey(to='enrichmentmanager.Teacher'),
        ),
        migrations.AddField(
            model_name='student',
            name='associated_teachers',
            field=models.ManyToManyField(blank=True, to='enrichmentmanager.Teacher', related_name='associated_teachers'),
        ),
        migrations.AddField(
            model_name='student',
            name='student',
            field=models.ForeignKey(to='academics.Student'),
        ),
        migrations.AddField(
            model_name='historicalteacher',
            name='teacher',
            field=models.ForeignKey(null=True, blank=True, related_name='+', to='academics.Teacher', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='advisor',
            field=models.ForeignKey(null=True, blank=True, related_name='+', to='enrichmentmanager.Teacher', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='history_user',
            field=models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='student',
            field=models.ForeignKey(null=True, blank=True, related_name='+', to='academics.Student', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalenrichmentsignup',
            name='student',
            field=models.ForeignKey(null=True, blank=True, related_name='+', to='enrichmentmanager.Student', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalenrichmentoption',
            name='teacher',
            field=models.ForeignKey(null=True, blank=True, related_name='+', to='enrichmentmanager.Teacher', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False),
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
            name='students',
            field=models.ManyToManyField(to='enrichmentmanager.Student', through='enrichmentmanager.EnrichmentSignup'),
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
