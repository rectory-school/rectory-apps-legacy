# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seating_charts', '0002_auto_20160203_1108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seatingstudent',
            old_name='foodAllergy',
            new_name='food_allerty',
        ),
    ]
