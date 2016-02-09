# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0024_auto_20151015_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrichmentsignup',
            options={'permissions': (('can_view_own_advisees', 'Can view own advisees'), ('can_view_other_advisees', "Can view other advisor's advisees"), ('can_view_all_advisees', 'Can view the full advisee lists'), ('can_edit_own_advisees', 'Can edit own advisee signups'), ('can_edit_all_advisees', 'Can edit all advisees signups'), ('can_edit_same_day', 'Can edit advisee signups on the same day'), ('can_view_reports', 'Can view reports'), ('can_view_single_student', 'Can view single student'), ('can_override_admin_lock', 'Can override admin lock'), ('can_set_admin_lock', 'Can set admin lock'))},
        ),
    ]
