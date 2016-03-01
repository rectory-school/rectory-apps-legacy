# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0003_auto_20160229_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detention',
            name='offense',
            field=models.ForeignKey(null=True, to='detention_notifier.Offense'),
        ),
    ]
