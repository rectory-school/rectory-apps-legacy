# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0032_auto_20160204_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalparent',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='parent',
            name='address',
            field=models.TextField(blank=True),
        ),
    ]
