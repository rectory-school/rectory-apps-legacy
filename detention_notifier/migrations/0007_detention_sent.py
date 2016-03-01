# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0006_auto_20160229_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='detention',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]
