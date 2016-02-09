# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0021_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrichmentsignup',
            name='enrichment_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='enrichmentmanager.EnrichmentOption'),
        ),
    ]
