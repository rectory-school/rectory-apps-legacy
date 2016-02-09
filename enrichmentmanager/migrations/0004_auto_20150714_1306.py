# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0003_enrichmentoption_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudent',
            name='nickname',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='nickname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
