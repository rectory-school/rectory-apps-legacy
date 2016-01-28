# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0013_iconlink_mac_pc_only'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iconlink',
            name='mac_pc_only',
        ),
        migrations.AddField(
            model_name='pageicon',
            name='mac_pc_only',
            field=models.BooleanField(verbose_name='Show on Windows/Mac only', default=False),
        ),
    ]
