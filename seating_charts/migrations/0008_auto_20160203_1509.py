# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seating_charts', '0007_auto_20160203_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ethnicity',
            options={'ordering': ['ethnicity']},
        ),
    ]
