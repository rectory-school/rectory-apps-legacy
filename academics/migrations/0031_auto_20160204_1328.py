# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0030_student_parents'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudentparentrelation',
            name='id_family_from',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name='studentparentrelation',
            name='id_family_from',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
