# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={},
        ),
        migrations.RenameField(
            model_name='historicalstudent',
            old_name='student',
            new_name='academic_student',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='student',
            new_name='academic_student',
        ),
    ]
