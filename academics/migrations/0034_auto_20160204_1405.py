# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0033_auto_20160204_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalparent',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, default=datetime.datetime(2016, 2, 4, 19, 5, 43, 882351, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 4, 19, 5, 47, 66397, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
