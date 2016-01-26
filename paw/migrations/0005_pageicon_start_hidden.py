# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0004_pageicon_check_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageicon',
            name='start_hidden',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
