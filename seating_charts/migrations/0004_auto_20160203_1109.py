# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seating_charts', '0003_auto_20160203_1108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seatingstudent',
            old_name='food_allerty',
            new_name='food_allergy',
        ),
    ]
