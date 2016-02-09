# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0034_auto_20160204_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalteacher',
            name='default_enrichment_description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='historicalteacher',
            name='default_enrichment_room',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='teacher',
            name='default_enrichment_description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='teacher',
            name='default_enrichment_room',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
