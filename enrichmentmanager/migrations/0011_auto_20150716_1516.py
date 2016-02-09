# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0010_auto_20150716_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]
