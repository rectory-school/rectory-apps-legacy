# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0006_auto_20151203_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='dorm',
            name='dorm_name',
            field=models.CharField(unique=True, default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dorm',
            name='area',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
