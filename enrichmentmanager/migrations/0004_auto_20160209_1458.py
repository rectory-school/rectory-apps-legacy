# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0003_auto_20160209_1243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrichmentoption',
            options={'ordering': ['teacher__academic_teacher__last_name', 'teacher__academic_teacher__first_name']},
        ),
    ]
