# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0008_auto_20150716_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='associated_teachers',
            field=models.ManyToManyField(related_name='associated_teachers', to='enrichmentmanager.Teacher'),
        ),
    ]
