# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0002_auto_20150119_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iconlink',
            name='url',
            field=models.CharField(max_length=4096),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='textlink',
            name='url',
            field=models.CharField(max_length=4096),
            preserve_default=True,
        ),
    ]
