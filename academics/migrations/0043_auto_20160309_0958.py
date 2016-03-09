# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0042_auto_20160309_0956'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalsection',
            old_name='section_course_name',
            new_name='course_name',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='section_course_name',
            new_name='course_name',
        ),
    ]
