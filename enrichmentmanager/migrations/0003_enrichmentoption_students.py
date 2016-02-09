# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0002_enrichmentoption_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrichmentoption',
            name='students',
            field=models.ManyToManyField(to='enrichmentmanager.Student', through='enrichmentmanager.EnrichmentSignup'),
        ),
    ]
