# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0014_detentionto'),
    ]

    operations = [
        migrations.AddField(
            model_name='offense',
            name='email_listing',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='detentionto',
            unique_together=set([('family_id_key', 'parent_code')]),
        ),
    ]
