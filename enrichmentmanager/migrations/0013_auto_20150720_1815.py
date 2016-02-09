# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0012_auto_20150716_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrichmentslot',
            name='allow_same_day_assign',
            field=models.BooleanField(verbose_name='Allow same day assignments universally', default=False),
        ),
        migrations.AddField(
            model_name='historicalenrichmentslot',
            name='allow_same_day_assign',
            field=models.BooleanField(verbose_name='Allow same day assignments universally', default=False),
        ),
    ]
