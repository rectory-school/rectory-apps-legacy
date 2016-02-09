# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0002_auto_20160209_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['academic_student__last_name', 'academic_student__first_name']},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['academic_teacher__last_name', 'academic_teacher__first_name']},
        ),
        migrations.RenameField(
            model_name='historicalteacher',
            old_name='teacher',
            new_name='academic_teacher',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='teacher',
            new_name='academic_teacher',
        ),
    ]
