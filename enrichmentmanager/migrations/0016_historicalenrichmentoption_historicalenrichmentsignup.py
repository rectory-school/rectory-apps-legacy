# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enrichmentmanager', '0015_auto_20150903_0532'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalEnrichmentOption',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True, verbose_name='ID', auto_created=True)),
                ('location', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=254)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='+', on_delete=django.db.models.deletion.SET_NULL)),
                ('slot', models.ForeignKey(null=True, to='enrichmentmanager.EnrichmentSlot', related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, db_constraint=False)),
                ('teacher', models.ForeignKey(null=True, to='enrichmentmanager.Teacher', related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, db_constraint=False)),
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
                ('id', models.IntegerField(blank=True, db_index=True, verbose_name='ID', auto_created=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('enrichment_option', models.ForeignKey(null=True, to='enrichmentmanager.EnrichmentOption', related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='+', on_delete=django.db.models.deletion.SET_NULL)),
                ('slot', models.ForeignKey(null=True, to='enrichmentmanager.EnrichmentSlot', related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, db_constraint=False)),
                ('student', models.ForeignKey(null=True, to='enrichmentmanager.Student', related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, db_constraint=False)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical enrichment signup',
                'get_latest_by': 'history_date',
            },
        ),
    ]
