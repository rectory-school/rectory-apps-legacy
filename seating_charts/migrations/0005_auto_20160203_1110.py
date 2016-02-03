# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seating_charts', '0004_auto_20160203_1109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seatingstudent',
            options={'ordering': ['enrollment__student__last_name', 'enrollment__student__first_name']},
        ),
    ]
