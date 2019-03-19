# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0043_auto_20160309_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='grade_level',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='historicalcourse',
            name='grade_level',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
