# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0022_auto_20150921_1241'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrichmentsignup',
            options={'permissions': (('can_view_own_advisees', 'Can view own advisees'), ('can_view_other_advisees', "Can view other advisor's advisees"), ('can_view_all_advisees', 'Can view the full advisee lists'), ('can_edit_own_advisees', 'Can edit own advisee signups'), ('can_edit_all_advisees', 'Can edit all advisees signups'), ('can_edit_same_day', 'Can edit advisee signups on the same day'), ('can_view_reports', 'Can view reports'), ('can_override_admin_lock', 'Can override admin lock'))},
        ),
        migrations.AddField(
            model_name='enrichmentsignup',
            name='admin_lock',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalenrichmentsignup',
            name='admin_lock',
            field=models.BooleanField(default=False),
        ),
    ]
