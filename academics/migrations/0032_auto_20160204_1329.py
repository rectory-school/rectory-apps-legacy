# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0031_auto_20160204_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalstudentparentrelation',
            name='id_family_from',
        ),
        migrations.RemoveField(
            model_name='studentparentrelation',
            name='id_family_from',
        ),
        migrations.AddField(
            model_name='historicalstudentparentrelation',
            name='family_id_key',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='studentparentrelation',
            name='family_id_key',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
