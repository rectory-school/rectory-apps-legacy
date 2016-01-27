# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import paw.models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0007_auto_20160126_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageicon',
            name='display_icon',
            field=versatileimagefield.fields.VersatileImageField(height_field='icon_height', upload_to=paw.models.iconUploadTo, width_field='icon_width'),
        ),
    ]
