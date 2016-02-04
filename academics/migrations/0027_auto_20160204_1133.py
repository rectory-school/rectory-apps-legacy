# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0026_auto_20160204_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='phone_cell',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='parent',
            name='phone_home',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='parent',
            name='phone_work',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
