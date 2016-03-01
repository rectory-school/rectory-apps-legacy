# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0039_auto_20160229_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudentparentrelation',
            name='parent_code',
            field=models.CharField(max_length=1, blank=True),
        ),
        migrations.AddField(
            model_name='studentparentrelation',
            name='parent_code',
            field=models.CharField(max_length=1, blank=True),
        ),
    ]
