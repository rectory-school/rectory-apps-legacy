# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0003_auto_20150217_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageicon',
            name='check_url',
            field=models.URLField(max_length=4096, blank=True),
            preserve_default=True,
        ),
    ]
