# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0017_auto_20160301_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='detentionmailer',
            name='do_not_send_same_day_before',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
