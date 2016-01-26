# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import paw.models


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageicon',
            name='display_icon',
            field=models.ImageField(height_field=b'icon_height', width_field=b'icon_width', upload_to=paw.models.iconUploadTo),
            preserve_default=True,
        ),
    ]
