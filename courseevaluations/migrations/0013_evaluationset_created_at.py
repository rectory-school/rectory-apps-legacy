# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0012_auto_20151209_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationset',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 12, 11, 15, 16, 52, 731404, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
