# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0014_auto_20150722_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrichmentoption',
            name='location',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
