# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0017_auto_20150916_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalteacher',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
