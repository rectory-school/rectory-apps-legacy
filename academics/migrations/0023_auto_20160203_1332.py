# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0022_auto_20160203_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudent',
            name='gender',
            field=models.CharField(blank=True, max_length=1, default=''),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, max_length=1, default=''),
        ),
    ]
