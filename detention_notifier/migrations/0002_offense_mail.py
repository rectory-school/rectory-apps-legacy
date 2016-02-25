# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offense',
            name='mail',
            field=models.BooleanField(default=True),
        ),
    ]
