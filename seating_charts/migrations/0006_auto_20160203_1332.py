# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seating_charts', '0005_auto_20160203_1110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tableassignment',
            options={'permissions': (('view_table_assignments', 'Can view table assignments'), ('edit_table_assignments', 'Can edit table assignments'))},
        ),
    ]
