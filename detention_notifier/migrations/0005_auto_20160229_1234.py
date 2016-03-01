# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0004_auto_20160229_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detention',
            name='detention_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='offense',
            name='sentence_insert',
            field=models.CharField(blank=True, max_length=4096),
        ),
    ]
