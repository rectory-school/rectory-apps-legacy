# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0041_auto_20160303_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsection',
            name='section_course_name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='section',
            name='section_course_name',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
