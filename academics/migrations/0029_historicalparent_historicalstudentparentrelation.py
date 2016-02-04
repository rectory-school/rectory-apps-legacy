# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0028_auto_20160204_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalParent',
            fields=[
                ('id', models.IntegerField(auto_created=True, verbose_name='ID', blank=True, db_index=True)),
                ('family_id', models.CharField(max_length=20)),
                ('parent_id', models.CharField(max_length=2)),
                ('full_id', models.CharField(max_length=22, db_index=True)),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('phone_home', models.CharField(max_length=100, blank=True)),
                ('phone_work', models.CharField(max_length=100, blank=True)),
                ('phone_cell', models.CharField(max_length=100, blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical parent',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStudentParentRelation',
            fields=[
                ('id', models.IntegerField(auto_created=True, verbose_name='ID', blank=True, db_index=True)),
                ('relationship', models.CharField(max_length=20, blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='academics.Parent', related_name='+')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='academics.Student', related_name='+')),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical student parent relation',
            },
        ),
    ]
