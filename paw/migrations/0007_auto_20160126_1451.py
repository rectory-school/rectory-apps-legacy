# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import paw.models


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0006_auto_20150717_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iconfoldericon',
            name='order',
            field=models.PositiveIntegerField(editable=False, default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='pageicon',
            name='display_icon',
            field=models.ImageField(width_field='icon_width', height_field='icon_height', upload_to=paw.models.iconUploadTo),
        ),
        migrations.AlterField(
            model_name='pageicondisplay',
            name='order',
            field=models.PositiveIntegerField(editable=False, default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='pagetextlink',
            name='order',
            field=models.PositiveIntegerField(editable=False, default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='pagetextlink',
            name='position',
            field=models.CharField(max_length=5, choices=[('LEFT', 'Left'), ('RIGHT', 'Right')]),
        ),
    ]
