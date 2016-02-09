# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0018_auto_20150917_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrichmentsignup',
            name='details',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='historicalenrichmentsignup',
            name='details',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
