# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0016_auto_20160301_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detentionmailer',
            old_name='signature',
            new_name='botton_section',
        ),
    ]
