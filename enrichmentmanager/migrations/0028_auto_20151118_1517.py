# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0027_auto_20151118_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalteacher',
            name='default_description',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='default_description',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
