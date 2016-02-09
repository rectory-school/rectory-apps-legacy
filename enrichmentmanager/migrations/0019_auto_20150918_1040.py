# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0018_auto_20150917_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrichmentslot',
            name='date',
            field=models.DateField(unique=True),
        ),
        migrations.AlterField(
            model_name='historicalenrichmentslot',
            name='date',
            field=models.DateField(db_index=True),
        ),
    ]
