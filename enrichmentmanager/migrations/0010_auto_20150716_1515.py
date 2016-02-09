# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0009_student_associated_teachers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='associated_teachers',
            field=models.ManyToManyField(to='enrichmentmanager.Teacher', related_name='associated_teachers', blank=True),
        ),
    ]
