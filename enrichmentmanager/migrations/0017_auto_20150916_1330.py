# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0016_historicalenrichmentoption_historicalenrichmentsignup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrichmentslot',
            name='allow_same_day_assign',
        ),
        migrations.RemoveField(
            model_name='historicalenrichmentslot',
            name='allow_same_day_assign',
        ),
        migrations.AddField(
            model_name='enrichmentslot',
            name='editable_until',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalenrichmentslot',
            name='editable_until',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
