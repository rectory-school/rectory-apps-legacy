# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0004_auto_20150714_1306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrichmentoption',
            options={'ordering': ['teacher__last_name', 'teacher__first_name']},
        ),
        migrations.AlterModelOptions(
            name='enrichmentsignup',
            options={'permissions': (('can_edit_own_advisees', 'Can edit own advisee signups'), ('can_edit_all_advisees', 'Can edit all advisees signups'), ('can_edit_same_day', 'Can edit advisee signups on the same day'))},
        ),
    ]
