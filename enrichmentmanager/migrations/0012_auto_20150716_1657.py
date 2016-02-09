# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0011_auto_20150716_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudent',
            name='lockout',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='lockout',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
