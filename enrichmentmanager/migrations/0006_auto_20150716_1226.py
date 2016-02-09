# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0005_auto_20150714_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrichmentsignup',
            options={'permissions': (('can_edit_own_advisees', 'Can edit own advisee signups'), ('can_edit_all_advisees', 'Can edit all advisees signups'), ('can_edit_same_day', 'Can edit advisee signups on the same day'), ('can_view_all_advisees', 'Can view the full advisee lists'))},
        ),
        migrations.AlterModelOptions(
            name='enrichmentslot',
            options={'ordering': ['date']},
        ),
    ]
