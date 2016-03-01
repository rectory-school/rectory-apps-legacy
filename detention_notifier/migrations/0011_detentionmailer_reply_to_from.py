# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0010_auto_20160229_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='detentionmailer',
            name='reply_to_from',
            field=models.BooleanField(default=True),
        ),
    ]
